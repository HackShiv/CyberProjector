import requests
import subprocess
import time

# Router login information
username = ""
password = "Blank"
router_ip = "192.168.1.254"

# Pi-hole IP address
pihole_ip = "192.168.1.100"

# Backup DNS servers to use if Pi-hole is down
backup_dns = "1.1.1.1, 1.0.0.1"

def check_pihole_status():
    try:
        # check if we can ping the pihole IP
        subprocess.run(["ping", "-n", "1", pihole_ip], check=True, capture_output=True)
        return True
    except:
        return False

# Login to the router
s = requests.Session()
data = {"":username, "ukk":password}
s.post("http://"+router_ip+"/login.cgi", data=data)

while True:
    if check_pihole_status():
        # set the Pi-hole IP address as the primary DNS
        data = {"dns1":pihole_ip}
        s.post("http://"+router_ip+"/dns.cgi", data=data)
        # configure the network adapter to use the Pi-hole IP as well as the backup DNS servers
        subprocess.run(["netsh", "interface", "ipv4", "set", "dnsservers", "name=", "Qualcomm Atheros QCA9377 Wireless Network Adapter #2", "source=static", "address=", pihole_ip + "," + backup_dns])
    else:
        # set the backup DNS servers as the primary DNS
        data = {"dns1":backup_dns.split(",")[0]}
        s.post("http://"+router_ip+"/dns.cgi", data=data)
        # configure the network adapter to use only the backup DNS servers
        subprocess.run(["netsh", "interface", "ipv4", "set", "dnsservers", "name=", "Qualcomm Atheros QCA9377 Wireless Network Adapter #2", "source=static", "address=", backup_dns])
    time.sleep(60)  # check the status of the Pi-hole every 60 seconds

# Logout
s.get("http://"+router_ip+"/logout.cgi")
