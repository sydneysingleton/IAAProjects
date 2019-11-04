import pandas as pd
import numpy as np
import sys

sys.path.insert( 1, "C:\\Users\\sydne\\Documents\\Python Scripts" ) #edit this to your own file path

from forecastiopy import *
import statistics as stat
def cityminmax(city, lat, long, api):
    cityDict = {'lat': lat, 'lon':long}
    weather = ForecastIO.ForecastIO( api, latitude=cityDict[ 'lat' ], longitude=cityDict[ 'lon' ] )
    daily=FIODaily.FIODaily( weather )
    d={}
    d["City"]=city
    for i in range(2,7):
         d["Min {0}".format(i-1)]=daily.get(i)['temperatureMin']
         d["Max {0}".format(i-1)]=daily.get(i)['temperatureMax']
    d["Avg Min"]=stat.mean([d["Min 1"], d["Min 2"], d["Min 3"], d["Min 4"], d["Min 5"]])
    d["Avg Max"]=stat.mean([d["Max 1"], d["Max 2"], d["Max 3"], d["Max 4"], d["Max 5"]])
    df1 = pd.DataFrame(d,index= [0])
    return(df1)
                          
api='52bee787c99d4d0fce9ba451d27848ae'
final = pd.concat([cityminmax("Anchorage, Alaska", 61.2181,-149.9003, api),
                   cityminmax("Buenos Aires, Argentina", -34.6037, -58.3816, api),
                   cityminmax("Sao Jose dos Campos, Brazil", -23.2237, -45.9009, api),
                   cityminmax("San Jose, Costa Rica",9.9281, -84.0907, api ),
                   cityminmax("Nanaimo, Canada",49.1659, -123.9401,api ),
                   cityminmax("Ningbo, China", 29.8683, 121.5440, api),
                   cityminmax("Giza, Egypt",30.0131, 31.2089, api ),
                   cityminmax("Mannaheim, Germany",49.4875, 8.4660, api),
                   cityminmax("Hyderabad, India",17.3850, 78.4867, api ),
                   cityminmax("Tehran, Iran",35.6892, 51.3890,api ),
                   cityminmax("Bishkek, Kyrgyzstan",42.8746, 74.5698, api ),
                   cityminmax("Riga, Latvia",56.9496, 24.1052,api ),
                   cityminmax("Quetta, Pakistan",30.1798, 66.9750, api ),
                   cityminmax("Warsaw,Poland",52.2297, 21.0122,api),
                   cityminmax("Dhahran, Saudia Arabia",52.2297, 21.0122,api ),
                   cityminmax("Madrid, Spain",40.4168, -3.7038,api ),
                   cityminmax("Oldham, United Kingdom",53.5409, -2.1114, api)])


print(final)

final.to_csv(r'C:\Users\sydne\Documents\darkskyFinal92.csv')

