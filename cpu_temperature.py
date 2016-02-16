#!/usr/bin/python
__author__ = 'f0xd3v1lsw1ld'
import os
import csv
import time
from time import localtime, strftime
import database_temperature

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
    
    timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
    gpu = getGpuTemperature()
    cpu = getCpuTemperature()
    ambient = getTemperature()
    
    temperature=[]
    temperature.append(timestamp)        
    temperature.append(gpu)
    temperature.append(cpu)
    temperature.append(ambient)
    
    writer.writerow(temperature)    
    file.close()
    
    database_temperature.insert_in_db("temperatures.db",timestamp, gpu, cpu, ambient )
        


main();
