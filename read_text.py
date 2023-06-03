import os
import time
import pandas as pd
from datetime import datetime
from data_analysis import analyse
os.system('clear')

def mac2ipv6(mac):
    # only accept MACs separated by a colon
    parts = mac.split(":")

    # modify parts to match IPv6 value
    parts.insert(3, "ff")
    parts.insert(4, "fe")
    parts[0] = "%x" % (int(parts[0], 16) ^ 2)

    # format output
    ipv6Parts = []
    for i in range(0, len(parts), 2):
        ipv6Parts.append("".join(parts[i:i+2]))
    ipv6 = "fe80::%s/64" % (":".join(ipv6Parts))
    return ipv6

def ipv62mac(ipv6):
    # remove subnet info if given
    subnetIndex = ipv6.find("/")
    if subnetIndex != -1:
        ipv6 = ipv6[:subnetIndex]

    ipv6Parts = ipv6.split(":")
    macParts = []
    for ipv6Part in ipv6Parts[-4:]:
        while len(ipv6Part) < 4:
            ipv6Part = "0" + ipv6Part
        macParts.append(ipv6Part[:2])
        macParts.append(ipv6Part[-2:])

    # modify parts to match MAC value
    macParts[0] = "%02x" % (int(macParts[0], 16) ^ 2)
    del macParts[4]
    del macParts[3]

    return ":".join(macParts)


def min_time(time1,time2):
    t1=time1.split(":")
    t2=time2.split(":")
    hour_1,min_1,sec_1=[float(t) for t in t1]
    hour_2,min_2,sec_2=[float(t) for t in t2]
    if(hour_1<hour_2):
        return time1
    elif(hour_1>hour_2):
        return time2
    else :
        if(min_1<min_2):
            return time1
        elif(min_1>min_2):
            return time2
        else :
            if(sec_1<sec_2):
                return time1
            elif(sec_1>sec_2):
                return time2


def extract_addr(router):
    files_path = "/home/techinix/Desktop/projet_ecole/cache/" 
    txt_path = files_path + "data.txt"
    users=pd.read_csv(files_path+"user_data.csv")
    while(True):
        systemCommand = "arp -a > " + txt_path
        os.system(systemCommand)
        with open(txt_path,"r") as file :
            Lines= file.readlines()
            for line in Lines:
                row = str(line).split(" ")
                if(len(row)<3):
                    continue
                read_time=str(datetime.now()).split(" ")[1]
                mac_addr=row[3]
                if(mac_addr in users["wifi_mac_addr"].tolist()):
                    try:
                        users.loc[users["wifi_mac_addr"]==mac_addr,[router+"_time"]]=min_time(users[users["wifi_mac_addr"]==mac_addr][router+"_time"].iloc[0],str(read_time))
                    except :
                        print(mac_addr,"error_wifi")

                elif(mac_addr in users["ipv6_generated_mac_addr"].tolist()):
                    try:
                        users.loc[users["ipv6_generated_mac_addr"]==mac_addr,[router+"_time"]]=min_time(users[users["ipv6_generated_mac_addr"]==mac_addr][router+"_time"].iloc[0],str(read_time))
                    except :
                        print("error_ipv6")
                else :
                    continue
        analyse(users)



extract_addr("r1")


