#!/usr/bin/python
import os
import csv
import time
from time import localtime, strftime

def getGpuTemperature():
 #use full path to use in cron job
 ret = os.popen('/opt/vc/bin/vcgencmd measure_temp').readline();
 temperature = ret.replace("temp=","").replace("'C\n","");
 
 return(float(temperature))

def getCpuTemperature():
 tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
 cpu_temp = tempFile.read()
 tempFile.close()
 return float(cpu_temp)/1000
 
def getTemperature():
 tempFile = open("/sys/bus/w1/devices/10-000802ac2e82/w1_slave")
 thetext = tempFile.read()
 tempFile.close()
 tempdata = thetext.split("\n")[1].split(" ")[9]
 temperature = float(tempdata[2:])
 temperature = temperature / 1000
 return temperature

def main(): 
          
    file = open("/home/pi/1-wire/rpi_temperature.csv","ab")
    writer = csv.writer(file,delimiter=',')
    temperature=[]
    temperature.append(strftime("%Y-%m-%d %H:%M:%S", localtime()))        
    temperature.append(getGpuTemperature())
    temperature.append(getCpuTemperature())
    temperature.append(getTemperature())
    writer.writerow(temperature)    
    file.close()
        


main();