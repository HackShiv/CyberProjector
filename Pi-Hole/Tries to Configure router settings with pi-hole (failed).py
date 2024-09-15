import requests
import subprocess
import time

username = ""
password = "Blank"
router_ip = "192.168.1.254"
pihole_ip = "192.168.1.100"
backup_dns = "1.1.1.1, 1.0.0.1"

def check_pihole_status():
    try:
        subprocess.run(["ping", "-n", "1", pihole_ip], check=True, capture_output=True)
        return True
    except:
        return False

s = requests.Session()
data = {"":username, "ukk":password}
s.post("http://"+router_ip+"/login.cgi", data=data)

while True:
    if check_pihole_status():
        data = {"dns1":pihole_ip}
        s.post("http://"+router_ip+"/dns.cgi", data=data)
        subprocess.run(["netsh", "interface", "ipv4", "set", "dnsservers", "name=", "Qualcomm Atheros QCA9377 Wireless Network Adapter #2", "source=static", "address=", pihole_ip + "," + backup_dns])
    else:
        data = {"dns1":backup_dns.split(",")[0]}
        s.post("http://"+router_ip+"/dns.cgi", data=data)
        subprocess.run(["netsh", "interface", "ipv4", "set", "dnsservers", "name=", "Qualcomm Atheros QCA9377 Wireless Network Adapter #2", "source=static", "address=", backup_dns])
    time.sleep(60) 
    
s.get("http://"+router_ip+"/logout.cgi")
