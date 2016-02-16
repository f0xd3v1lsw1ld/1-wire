#!/usr/bin/python
__author__ = 'f0xd3v1lsw1ld'

#SELECT timestamp, avg(ambient) FROM temperature WHERE timestamp BETWEEN "2015-03-29 " AND "2015-03-30"
import sqlite3
import csv
import sys
import os
import argparse
import datetime

sql_insert_temperature = "INSERT OR IGNORE INTO temperature VALUES (?, ?, ?, ?)"

def insert_in_db(database, timestamp, gpu, cpu, ambient):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS temperature(timestamp DATETIME, gpu NUMERIC, cpu NUMERIC, ambient NUMERIC, UNIQUE(timestamp))""")
    connection.commit()
    cursor.execute(sql_insert_temperature,(timestamp, gpu, cpu, ambient) ) 
    connection.commit()
    connection.close()
    
    

def insert_csv_in_db(path):

    connection = sqlite3.connect("temperatures.db")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS temperature(timestamp DATETIME, gpu NUMERIC, cpu NUMERIC, ambient NUMERIC, UNIQUE(timestamp))""")
    connection.commit()
    
    for fn in os.listdir(path):
        
        if fn.endswith(".csv") and os.path.isfile(path+"/"+fn):
            try:
                reader = csv.reader(open(path+"/"+fn,"r"), delimiter=",")
                temp_list = list(reader)
                for item in temp_list:                  
                    input = item
                    cursor.execute(sql_insert_temperature, input)                  
    
            except Exception as e:
                print(str(e))
        else:
            continue
        
        connection.commit()
    connection.close()

def select_from_db(min, max, avg, start, end):      
    sql_select_avg = "SELECT avg(ambient) FROM temperature"
    sql_select_avg_range = "SELECT avg(ambient) FROM temperature WHERE timestamp BETWEEN '%s' AND '%s'"
    
    sql_select_min = "SELECT timestamp, min(ambient) FROM temperature"
    sql_select_min_range = "SELECT timestamp, min(ambient) FROM temperature WHERE timestamp BETWEEN '%s' AND '%s'"
    
    sql_select_max = "SELECT timestamp, max(ambient) FROM temperature"
    sql_select_max_range = "SELECT timestamp, max(ambient) FROM temperature WHERE timestamp BETWEEN '%s' AND '%s'"
    
    
    connection = sqlite3.connect("temperatures.db")
    cursor = connection.cursor()
    
    if True is min:
        select_cmd = sql_select_min
        
        if start is not None and end is not None:            
            select_cmd = sql_select_min_range % (start, end)
        elif start is not None:
            date = datetime.datetime.strptime(start,"%Y-%m-%d")           
            date += datetime.timedelta(days=1)           
            select_cmd = sql_select_min_range % (start, date)
            
        cursor.execute(select_cmd)    
        minvalue = cursor.fetchone()
        print("MIN: %s C at %s" % (str(minvalue[1]), str(minvalue[0])))
    if True is max:
        select_cmd = sql_select_max
        
        if start is not None and end is not None:            
            select_cmd = sql_select_max_range % (start, end)
        elif start is not None:
            date = datetime.datetime.strptime(start,"%Y-%m-%d")           
            date += datetime.timedelta(days=1)           
            select_cmd = sql_select_max_range % (start, date)
         
        cursor.execute(select_cmd)
        maxvalue = cursor.fetchone()
        print("MAX: %s C at %s" % (str(maxvalue[1]), str(maxvalue[0])))
        
    if True is avg:
        select_cmd = sql_select_avg
        
        if start is not None and end is not None:            
            select_cmd = sql_select_avg_range % (start, end)
        elif start is not None:
            date = datetime.datetime.strptime(start,"%Y-%m-%d")           
            date += datetime.timedelta(days=1)           
            select_cmd = sql_select_avg_range % (start, date)   
    
        cursor.execute(select_cmd)
        maxvalue = cursor.fetchone()
        print("AVERAGE: %.2f C " % (maxvalue[0]))
    
    connection.close()
    
def print_db(start, end):
    sql_select = "SELECT timestamp, ambient FROM temperature"
    sql_select_range = "SELECT timestamp, ambient FROM temperature WHERE timestamp BETWEEN '%s' AND '%s'"
    
    
    connection = sqlite3.connect("temperatures.db")
    cursor = connection.cursor()
    select_cmd = sql_select
    
    if start is not None and end is not None:            
            select_cmd = sql_select_range % (start, end)
    elif start is not None:
        date = datetime.datetime.strptime(start,"%Y-%m-%d")           
        date += datetime.timedelta(days=1)           
        select_cmd = sql_select_range % (start, date)   
    
    cursor.execute(select_cmd)
    for entry in cursor:
        print(entry[0],entry[1])  
        
    #entries=cursor.fetchall()

    connection.close()    

    #return entries       
    
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", action='store_true', default=False,
                    dest='import_switch', help="import all csv files of current dir")
    parser.add_argument('-d', action='store',default="./", dest='directory',
                    help='set working directory')
    parser.add_argument("--min", action='store_true', default=False,
                    dest='get_min', help="show mininmal value")
    parser.add_argument("--max", action='store_true', default=False,
                    dest='get_max', help="show maximal value")
    parser.add_argument("--avg", action='store_true', default=False,
                    dest='get_avg', help="show average value")  
    parser.add_argument('-s', action='store',default=None, dest='start',
                    help='set start date YYYY-MM-DD')
    parser.add_argument('-e', action='store',default=None, dest='end',
                    help='set end date YYYY-MM-DD') 
    parser.add_argument('-p', action='store_true',default=False, dest='print_values',
                    help='print values')
                    
    try:                
        results = parser.parse_args()
    except Exception as e:
        parser.print_help()
        return
    if True is results.import_switch:
        insert_csv_in_db(results.directory)
    elif True is results.get_min or True is results.get_max or True is results.get_avg:
        select_from_db(results.get_min, results.get_max, results.get_avg, results.start, results.end)
    elif True is results.print_values:
        print_db(results.start, results.end)
    else:
        parser.print_help()
        
    



if __name__ == "__main__":
    main()
