import os
import psutil
import socket
import subprocess

# Define password
password = "Y7r$9VwLz@2bTpA#q1E3X"

# Function to get current connected IPs on the LAN
def get_connected_ips():
    # Obtain all network interfaces
    connected_ips = []
    for conn in psutil.net_connections(kind='inet'):
        ip = conn.raddr.ip if conn.raddr else None
        if ip and ip not in connected_ips:
            connected_ips.append(ip)
    return connected_ips

# Function to check if system is connected to LAN
def check_lan_connection():
    try:
        # Attempt to resolve a known LAN server or external address
        socket.create_connection(('8.8.8.8', 80), timeout=5)
        return True  # System is connected to LAN
    except OSError:
        return False  # No connection

# Function to disable network driver
def disable_network_driver():
    # Disable all network adapters by interfacing with system commands
    try:
        subprocess.run("powershell -Command \"Get-NetAdapter | Disable-NetAdapter -Confirm:$false\"", check=True, shell=True)
        print("Network drivers disabled.")
    except Exception as e:
        print(f"Error disabling network drivers: {e}")

# Function to enable network driver
def enable_network_driver():
    try:
        subprocess.run("powershell -Command \"Get-NetAdapter | Enable-NetAdapter -Confirm:$false\"", check=True, shell=True)
        print("Network drivers enabled.")
    except Exception as e:
        print(f"Error enabling network drivers: {e}")

# Function to check the network access count (number of systems)
def check_network_access():
    # Get current connected IPs
    connected_ips = get_connected_ips()
    print(f"Currently connected systems: {len(connected_ips)}")
    return len(connected_ips)

# Function to request password and handle conditions
def handle_access_control():
    entered_password = input("Enter password: ")
    
    if entered_password == password:
        if check_lan_connection():
            print("System connected to LAN.")
            systems_connected = check_network_access()
            
            if systems_connected > 2:
                print("More than 2 systems connected. Disabling network.")
                disable_network_driver()  # Disable network if over 2 systems
            else:
                print("Network is within access limit.")
        else:
            print("No LAN connection detected.")
    else:
        print("Incorrect password.")

# Run the access control system
handle_access_control()
