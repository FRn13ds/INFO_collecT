import socket
import subprocess
import json
from colorama import *
import time
import os

admin_name = "FRn13ds"
password = "014014"

User_ = str(input("Admin Name :"))
pass_ = str(input("Password :"))
if admin_name == User_ and pass_ == password:
    c = 0
    for i in range(100):
        c = c + 1
        print("collecting information...", c, "%")
        time.sleep(0.1)  # استخدم time.sleep بدلاً من os.system('cls') لأن 'cls' غير موجودة في Termux

# Signal Logo
def draw_signal_logo():
    logo = """
        ███████╗██╗  ██╗██╗██╗     ██╗      █████╗ ██╗      ██████╗ 
        ██╔════╝██║  ██║██║██║     ██║     ██╔══██╗██║     ██╔════╝ 
        █████╗  ███████║██║██║     ██║     ███████║██║     ██║  ███╗
        ██╔══╝  ██╔══██║██║██║     ██║     ██╔══██║██║     ██║   ██║
        ██║     ██║  ██║██║███████╗███████╗██║  ██║███████╗╚██████╔╝
        ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ 
    """
    print(Fore.RED + logo)

draw_signal_logo()
print(Fore.RED + "Please Open Your Hotspot!")

def get_connected_devices():
    # Get the IP address of the hotspot
    ip_address = subprocess.check_output("ip -4 addr show wlan0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'", shell=True).decode().strip()
    
    # Get the list of connected devices
    devices = subprocess.check_output(f"arp-scan --interface=wlan0 --localnet", shell=True).decode().strip().split('\n')[2:]
    
    connected_devices = []
    
    for device in devices:
        parts = device.split()
        if len(parts) >= 2:
            ip = parts[0]
            mac = parts[1]
            try:
                # Get the hostname
                name = socket.gethostbyaddr(ip)[0]
            except socket.herror:
                name = "Unknown"
            
            connected_devices.append({
                "IP Address": ip,
                "MAC Address": mac,
                "Device Name": name
            })
    
    return connected_devices

def check_hotspot_status():
    # Check if the hotspot is active
    result = subprocess.run(["nmcli", "dev", "status"], capture_output=True, text=True)
    return "wlan0" in result.stdout

if __name__ == "__main__":
    if check_hotspot_status():
        devices_info = get_connected_devices()
        print(json.dumps(devices_info, indent=4))
    else:
        print("Hotspot is not active.")
else:
    print("please Contact The GitHub page admin to get information!")
