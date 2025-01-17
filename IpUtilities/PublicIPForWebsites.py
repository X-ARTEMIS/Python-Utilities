import socket

def get_public_ip(website_url):
    try:
        ip_address = socket.gethostbyname(website_url)
        return ip_address
    except socket.gaierror:
        return "Invalid website URL"

if __name__ == "__main__":
    website_url = input("Enter the website URL (e.g., example.com): ")
    public_ip = get_public_ip(website_url)
    print(f"The public IP address of {website_url} is: {public_ip}")
