import subprocess

subprocess.run(["curl", "-L", "https://install.pi-hole.net/repo.pi-hole.org/pi-hole-64bit-install.exe", "-o", "pi-hole-64bit-install.exe"])

subprocess.run(["./pi-hole-64bit-install.exe", "-install"])

ip_address = subprocess.run(["ipconfig"], capture_output=True).stdout.decode().split("IPv4 Address. . . . . . . . . . . :")[1].split("\n")[0].strip()

subprocess.run(["pihole", "-a", "ipconfig", ip_address])

