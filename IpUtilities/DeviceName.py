import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

print("Your Computer Name is: " + hostname)