import subprocess

# Download the Pi-hole installer for Windows
subprocess.run(["curl", "-L", "https://install.pi-hole.net/repo.pi-hole.org/pi-hole-64bit-install.exe", "-o", "pi-hole-64bit-install.exe"])

# Run the installer
subprocess.run(["./pi-hole-64bit-install.exe", "-install"])

# Get the IP address of the machine
ip_address = subprocess.run(["ipconfig"], capture_output=True).stdout.decode().split("IPv4 Address. . . . . . . . . . . :")[1].split("\n")[0].strip()

# Configure Pi-hole to use the IP address as the DNS server
subprocess.run(["pihole", "-a", "ipconfig", ip_address])

