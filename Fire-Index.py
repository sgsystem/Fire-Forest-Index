#!/usr/bin/env python3#

import math
import time

#Create by Tsvetomir Gotsov
#
#input variable

temperature = input("Temperature at noon, C: \n")
temperature = int(temperature)
humidity = input("Relative humidity at noon, %: \n")
humidity = int(humidity)
wind_speed = input("Wind Speed at noon:,km/h: \n")
wind_speed = int(wind_speed)
daily_rain = input("Daily rain, mm: \n")
daily_rain = int(daily_rain)

#print (temperature,humidity,wind_speed,daily_rain)

##############################################################################
# Time
t = time.time()
tm = time.gmtime(t)
mon = tm.tm_mon
#print (mon)

##############################################################################
# Effective_daylengts for Sofia, Bulgaria 2014
Effective_daylengts = [9.5, 10.4, 11.5, 13.5, 14.5, 15.16, 14.83, 13.5, 12.5, 11.5, 9.66, 9.16]
Le = Effective_daylengts [mon - 1]
#print(Le)

##############################################################################
#Intial Spread Index

pow_wf = (0.05039*float(wind_speed))
#wf = pow(2.718281828459,pow_wf)
wf = math.exp(pow_wf) #Compute wind-factor
print("wf=",wf)

m = 1.0 #Water content in fine fuel after the drainage ???
buffer_var1 = 91.9*math.exp((-0.1386*m))
buffer_var2 = pow(m,5.31)
buffer_var3 = pow(10,7)*4.93
ffh = buffer_var1 * (1+(buffer_var2/buffer_var3)) #Compute Fine fuel humidity factor

print("ffh=",ffh)

R = 0.208*wf*ffh #Index 1

print("R=",R)
buffer_R = int(R)
if buffer_R==0 | buffer_R==1:
    print("Ниска степен на разпространение на пожар")
elif buffer_R>=2 & buffer_R<= 10:
    print("Висока степен от разпространение на пожар")
elif buffer_R>10:
    print("Изключително бърз темп на разпространение на пожари")

##############################################################################
#Code 2 Duff moisture Code
P0 = 10 #Код 2 от предишния ден
daily_rain = float(daily_rain)
if daily_rain > 1.5:
    re = (0.92*daily_rain)-1.27
else:
    re = daily_rain

buffer_var4 = math.exp(5.6348-(0.023*P0))
M0 = 20 + buffer_var4
b = 0
if P0<=33:
    b = 100/(0.5+0.3*P0)
elif  P0>33 | P0<=65:
    b = 14 - 1.3*(math.log(P0))
else:
    b = 6.2*(math.log(P0))-17.2
    
#### Compute Water Comtent in duff after the rain
buffer_var5 = 1000*re
buffer_var6 = 48.77+b*re
Mr=M0+(buffer_var5/buffer_var6)
##### Compute Code 2 in duff after the rain
Pr = 244.72 - 43.43 * math.log(Mr-20)

if Pr <0:
    Pr = 0
else:
    Pr = P0
#### Determinate Effective day length Code 2 in hours Le
#Le = 10
minimum_value = -1.1
#### Compute Logarithmic drainage speed Code 2
if float(temperature) <= minimum_value:
    temperature = -1.1
K = 1.894*(float(temperature)+1.1)*(100-float(humidity))*Le*pow(10,-6)
P = P0 + 100*K
print("P=",P)
#if float(P) >= 30 & float(P) <= 39:
#    print("сухо")
#elif float(P)>=40:
#    print("интензивно горене")
#else:
#    print("Няма опасност от интензивно горене")

#############################################################
#Drought Code
# Code 3
# This is new --> 23.09.2015
if daily_rain > 2.8:
    real_rain_code_3 = 0.83*daily_rain - 1.27
#else:
#    daily_rain = real_rain_code_3

# Compute Equivalent humidity of Code 3 of previous day
D0=5 ## Temp value
Q0 = 800*math.exp(-D0*0.0025) #Compute Equivalent humidity of Code 3 previos the rain
Qr = Q0 + (3.937*real_rain_code_3) #Compute Equivalent humidity of Code 3 after the rain
buffer_var7 = 800/Qr
Dr = 400*math.log(buffer_var7) #Compute Code 3 after the rain
if Dr < 0:
    Dr = 0
else:
    Dr = D0
Lf = 200 #Determinate Effective day length Code 3 in hours !!!
if temperature < -2.8:
    temperature = -2.8
else:
    V = 0.36 * (temperature + 2.8) + Lf #Compute Potential evapotranspiration
if V < 0:
    V = 0
D = D0 + 0.5 * V #Compute D in function of D0


###################################################################
#Code 1
#Fine Fuel Moisture
#



    


    





