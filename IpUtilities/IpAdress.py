import requests

Warn = input("WARNING: THIS WILL SHOW YOUR REAL IP ADRESS AND WE ARE NOT RESPONSABLE FOR WHAT HAPPENS, ARE YOU SURE YOU WOULD LIKE TO PASS [Y] [N]: ")
if Warn == "Y":
    def get_public_ip():

        response = requests.get('https://api64.ipify.org?format=json')

        ip_address = response.json()['ip']

        return ip_address

    print("Your public IP address is:", get_public_ip(), "(DO NOT SHARE THIS)")

if Warn == "N":
    print("You have not accepted the warn, goodbye.")
    exit()