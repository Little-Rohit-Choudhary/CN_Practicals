from getmac import get_mac_address as gmd
print("MAC address of the system: ",gmd())

#Displaying local IP address
import socket
hostname = socket.gethostname()
print("Hostname: ",hostname)
local_ip = socket.gethostbyname(hostname)
print(f"Local IP Address: {local_ip}")