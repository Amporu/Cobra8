import threading
import subprocess
import time
import numpy as np
class DataThread(threading.Thread):
    def __init__(self, label):
        super().__init__()
        self.label = label
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            self.get_data()
            time.sleep(1)  # Add a delay between updates

    def stop(self):
        self.stop_event.set()

    def get_data(self):
        try:
            total_ram_gb = DataThread.get_total_ram()
            #print("total_ram " + str(total_ram_gb))
        except Exception as e:
            print(e)

        try:
            device_model_name = subprocess.run(
                ["adb", "shell", "getprop", "ro.product.model"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            ).stdout.strip()
            if device_model_name is not None:
                #self.label.info_id_label.config(foreground="white")
               # self.label.info_id_label.config(text="ID: ", foreground="green")
                self.label.id_data_label.config(text=device_model_name)
                
            # ADB command to get CPU architecture
            adb_command = "adb shell getprop ro.product.cpu.abi"

            try:
                # Run the ADB command and capture the output
                output = subprocess.check_output(adb_command, shell=True, text=True)
                
                # Extract and print only the CPU architecture
                cpu_architecture = output.strip()
                self.label.arch_data_label.config(text=str(cpu_architecture))
                #print(cpu_architecture)
            except subprocess.CalledProcessError as e:
                print("Error:", e)
        except Exception as e:
            print(e)

        try:
            cmd_cpu = ["adb", "shell", "dumpsys", "cpuinfo"]
            result_cpu = subprocess.run(cmd_cpu, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            cpu_percentage = None

            lines_cpu = result_cpu.stdout.splitlines()
            for line in lines_cpu:
                if "TOTAL:" in line:
                    total_line = line.split("TOTAL:")[1].strip()
                    percentages = total_line.split()[1:-1]
                    numeric_percentages = [p for p in percentages if p.endswith("%")]
                    cpu_percentage = sum(float(p.strip("%")) for p in numeric_percentages)

            if cpu_percentage is not None:
                self.label.cpu_data_label.config(text=str(np.around(float(cpu_percentage),2)))
            else:
                print("CPU(%):")

        except Exception as e:
            print("CPU:"+str(e))

        
        cmd_ram = ["adb", "shell", "dumpsys", "meminfo"]
        result_ram = subprocess.run(cmd_ram, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        ram_usage_kb = None

        if result_ram.returncode == 0:
            for line in result_ram.stdout.splitlines():
                if "Used RAM:" in line:
                    ram_usage_str = line.split(":")[1].strip().replace(",", "")
                    ram_usage_kb = int(ram_usage_str.split("K")[0])

            # Convert RAM usage to GB
            if ram_usage_kb is not None:
                ram_usage_gb = ram_usage_kb / 1048576  # Convert KB to GB
                #print("OK")
                total_ram_gb_str = f"{total_ram_gb:.2f}" if total_ram_gb is not None else "N/A"
                self.label.ram_data_label.config(text=str(np.around(float(ram_usage_gb),2))+"GB /" +str(np.around(float(total_ram_gb),2))+"GB")
                #print(f"RAM Usage: {ram_usage_gb:.2f}GB / {total_ram_gb_str}GB")
            else:
                print("RAM Usage:")
        

    @staticmethod
    def get_total_ram():
        # Get total RAM
        total_ram_cmd = ["adb", "shell", "cat", "/proc/meminfo"]
        result_total_ram = subprocess.run(total_ram_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        total_ram_kb = None

        if result_total_ram.returncode == 0:
            for line in result_total_ram.stdout.splitlines():
                if line.startswith("MemTotal:"):
                    total_ram_str = line.split()[1]
                    total_ram_kb = int(total_ram_str)
        # Convert total RAM to GB
        if total_ram_kb is not None:
            total_ram_gb = total_ram_kb / 1048576  # Convert KB to GB
            return total_ram_gb
        else:
            return None
