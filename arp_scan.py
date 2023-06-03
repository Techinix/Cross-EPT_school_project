import os
import time
import pandas as pd
os.system('clear')


def detect_addr():
    
	files_path = "/home/techinix/Desktop/projet_ecole/cache/" 
	txt_path = files_path + "data.txt"
	while(True):
		systemCommand = "arp -a > "+ txt_path
		os.system(systemCommand)
		print(time.time())
		



detect_addr()