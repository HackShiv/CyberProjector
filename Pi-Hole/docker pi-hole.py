import subprocess
import time

subprocess.run("powershell.exe -Command \"Invoke-WebRequest -Uri https://get.docker.com -OutFile $env:TEMP\\docker-install.ps1\"", shell=True)
subprocess.run("powershell.exe -Command \"& $env:TEMP\\docker-install.ps1\"", shell=True)
subprocess.run("powershell.exe -Command \"Start-Service Docker\"", shell=True)
subprocess.run("docker pull pihole/pihole", shell=True)
subprocess.run("docker run --name pihole -p 53:53/tcp -p 53:53/udp -p 80:80 -p 443:443 -e TZ='Europe/London' -e WEBPASSWORD='<Riderzz2005!>' --dns=127.0.0.1 --dns=1.1.1.1 -v /etc/pihole/:/etc/pihole/ -v /etc/dnsmasq.d/:/etc/dnsmasq.d/ --restart=unless-stopped -d pihole/pihole", shell=True)

while True:
    pihole_status = subprocess.run("docker inspect -f '{{.State.Running}}' pihole", shell=True, capture_output=True)
    if pihole_status.stdout.decode("utf-8") == "true\n":
        print("pi-hole is online, using pi-hole as DNS")
    else:
        print("pi-hole is offline, using 1.1.1.1 and 1.0.0.1 as backup DNS")
        subprocess.run("powershell.exe -Command \"Set-DnsClientServerAddress -InterfaceIndex (Get-NetAdapter).ifIndex -ServerAddresses 1.1.1.1,1.0.0.1\"", shell=True)
    time.sleep(30)

