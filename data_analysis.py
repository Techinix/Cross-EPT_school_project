import pandas as pd
from datetime import datetime
def str2time(s):
    hour,min,sec=[float(t) for t in s]
    t_sec=hour*3600 + min*60 + sec
    return t_sec
def diff_time(r_time1,r_time2):#(t1-t2)
    t1=r_time1.apply(lambda t : str2time(t.split(":")))
    t2=r_time2.apply(lambda t : str2time(t.split(":")))
    return t1-t2

def analyse(users):
    files_path = "/home/techinix/Desktop/projet_ecole/cache/" 
    checkpoints_data=pd.read_csv(files_path+"checkpoints_data.csv")
    routers=[]
    for col in users.columns :
        if("_" in col):
            col=col.split("_")
            if len(col)==2 and col[1]=="time":
                routers.append(col)
    avg_speed=0
    for i in range(len(routers)-1):
        users["r"+str(i+1)+"_r"+str(i+2)+"_segment_average_speed"]=(int(checkpoints_data["r_"+str(i+2)][0])-int(checkpoints_data["r_"+str(i+1)][0]))/diff_time(users["r"+str(i+2)+"_time"],users["r"+str(i+1)+"_time"])
        avg_speed+=users["r"+str(i+1)+"_r"+str(i+2)+"_segment_average_speed"]
    avg_speed/=(len(routers)-1)
    users["total_average_speed"]=avg_speed
    users.to_csv(files_path+"users_data_processed.csv",index=False)
