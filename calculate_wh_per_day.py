import csv
import re
import time
import sys
import datetime
import logging
import logging.handlers
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time

## Read CSV
data = pd.read_csv('yourCSV.log', sep=" ", header = None)

## Remove any pesky NaNs
data = data.dropna()

## Name each column
data.columns = ["Date", "Time", "Plug", "MAC Address", "Watts", "At", "UNIX Time" ]

# Remove nanoseconds from time (not needed...) data['Time'] = [x.split(',')[0] for x in data['Time']]

## Combine date, time and watts.
data["DateTime"] = data["Date"].map(str) + " " + data["Time"]

data["DateTime"] = pd.to_datetime(data['DateTime'])

data["DateTimeWatts"] = data["Date"].map(str) + " " + data["Time"].map(str) + " " + data["Watts"].map(str)


## Get dates from log
uniqueDates = np.unique(data.Date)
uniquePlug = np.unique(data.Plug)


print(uniqueDates)
print(uniquePlug)

## Method to calc Wh
def calcWh(self, uniqueDates, uniquePlug):

    totalinWh = []
    i = 0
    plugs = 0

    for j in range (len(uniquePlug)):

        thisDevice = data[data['Plug'].isin([uniquePlug[plugs]])]
        thisDevice = thisDevice.reset_index(drop=True)
        dates = 0
        index = 0


        for i in range(len(uniqueDates)):


                total = 0
                ## Get days
                thisDate = data[data['Date'].isin([uniqueDates[dates]]) & data['Plug'].isin([uniquePlug[plugs]])]
                print(thisDate)

                thisDate = thisDate.reset_index(drop=True)

                #print((len(thisDate)-1))

                for k in range(len(thisDate)-1):

                    ## Get Watts
                    value1 = thisDate.Watts[k]
                    value2 = thisDate.Watts[k+1]

                    totalWatts = (value1 + value2)/2
                    ## Get Times
                    time1 = thisDate.DateTime[k]

                    time2 = thisDate.DateTime[k+1]

                    ## Calculate difference in time
                    time = pd.Timedelta(time2 - time1).seconds
                    #print(time, totalWatts)

                    sumtotal = time * totalWatts

                    total = total + sumtotal
                    #print(time, sumtotal, total)
                    #print(min(wtts),max(wtts))
                    theDay = uniqueDates[index]


                theDevice = uniquePlug[plugs]

                total = total/3600

                result = [theDevice, theDay, total]

                totalinWh.append(result)
        
                index = index + 1
        
                dates = dates + 1

        plugs = plugs + 1

    return totalinWh    

totalinWh = calcWh(data.DateTimeWatts, uniqueDates, uniquePlug)

totalinWh = np.array(totalinWh)
totalinWh = pd.DataFrame(totalinWh)

totalinWh.to_csv('output.csv', sep=',', index=False, header=False)


