#!/usr/bin/env python3#

import math
import time

#Create by Tsvetomir Gotsov
#
#input variable

temperature = float(input("Temperature at noon, C: \n"))
humidity = float(input("Relative humidity at noon, %: \n"))
wind_speed = float(input("Wind Speed at noon:,km/h: \n"))
daily_rain = float(input("Daily rain, mm: \n"))

#print (temperature,humidity,wind_speed,daily_rain)
rf = 0.1 # Purvonachalna inicializaciq, no trqbwa da go mahna?
F0 = 10    #Probno ???
##############################################################################
# Time
t = time.time()
tm = time.gmtime(t)
mon = tm.tm_mon
#print (mon)

##############################################################################
# Effective_daylengts for Sofia, Bulgaria 2014
# http://www.nao-rozhen.org/astrocalendar/2014/sun_and_moon.htm
Effective_daylengts = [9.5, 10.4, 11.5, 13.5, 14.5, 15.16, 14.83, 13.5, 12.5, 11.5, 9.66, 9.16]
Le = Effective_daylengts [mon - 1]
#print(Le)

##############################################################################
#Code 1
#Fine Fuel Moisture Code (FFMC)
# m0 - Water content in fine fuel of the previous day
# mr - Water content in fine fuel after the rain
# m - water content in fine fuel after the drainage
# rf - real rain, FFMC
# Ed - TEE (equilibrium water content) of fine fuel after the drainage
# Ew - TEE (equilibrium water content) of fine fuel after moistening
# k0 - intermediate value of kd
# kd - logarithmic drainage speed, FFMC, Log10 m/day
# k1 - intermediate value of kw
# kw - logarithmic moisture speed, Log10 m.day
# F - FFMC
# F0 - FFMC of the previous day

m0 = 147.2*(101-F0)/(59.5+F0)
print("m0",m0)
if(daily_rain < 0,5):
    rf = daily_rain
else:
    rf = daily_rain - 0.5
print("rf",rf)

if m0 <= 150:
    buffer_var2 = 251 - m0
    buffer_var3 = -100/buffer_var2
    buffer_var4 = pow(2.73,buffer_var3)
    buffer_var5 = -6.93/rf
    buffer_var6 = pow(2.73,buffer_var5)
    buffer_var7 = 1 - buffer_var6
    buffer_var1 = buffer_var4 * buffer_var7
    mr = m0 + (42.5*rf*buffer_var1)
elif (m0 > 150) & (m0 <250):
    buffer_var2 = 251 - m0
    buffer_var3 = -100/buffer_var2
    buffer_var4 = pow(2.73,buffer_var3)
    buffer_var5 = -6.93/rf
    buffer_var6 = pow(2.73,buffer_var5)
    buffer_var7 = 1 - buffer_var6
    buffer_var1 = buffer_var4 * buffer_var7
    buffer_var8 = pow(m0-150,2)
    buffer_var9 = pow(rf,0.5)
    mr = m0 + (42.5*rf*buffer_var1) + (0.0015*buffer_var8*buffer_var9)
    #mr = m0 + (42.5*rf*buffer_var1)+(0.0015*(pow(m0-150,2)*pow(rf,0.5)))
else:
    mr = m0
print("mr = ", mr)




#Code 2
#Duff Moisture Code (DMC)
# M0 - Water content in duff of the previous day
# Mr - Water content in duff after the Rain
# M - Water content in duff after the drainage
# K - Logarithmic drainage speed, DMC, Log10 m/day
# re - Real rain, DMC
# Le - Effective day length DMC, hour
# b - Slope factor in DMC
# P0 - DMC of the previous day
# Pr - DMC after the rain
# P - DMC

P0 = 10 #Код 2 от предишния ден
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
if temperature <= minimum_value:
    temperature = -1.1
K = 1.894*(temperature+1.1)*(100-humidity)*Le*pow(10,-6)
P = P0 + 100*K
print("Code 2 Duff Moisture P=",P)
#if float(P) >= 30 & float(P) <= 39:
#    print("сухо")
#elif float(P)>=40:
#    print("интензивно горене")
#else:
#    print("Няма опасност от интензивно горене")

#############################################################
#Drought Code (DC)
# Code 3
# This is new --> 23.09.2015
# Q - equivalent humidity of DC, multiple di 0.254 mm
# Q0 - quivalent humidity of DC of the previous day
# Qr - quivalent humidity after the rain
# rd - real rain, DC
# V - Potential evapotranspiration, multiple of 0.254 mm of water/day
# Lf - effective day length DC, hours
# D0 - DC of the previous day
# Dr after the rain
# D
if daily_rain > 2.8:
    real_rain_code_3 = 0.83*daily_rain - 1.27
else:
    real_rain_code_3 = daily_rain

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


##############################################################################
#Intial Spread Index (ISI)
#Index 1
# f(W) - wind factor
# f(F) - fine fuel humidity factor
# m - water content in fine fuel after the drainage
# R - ISI

pow_wf = (0.05039*wind_speed)
#wf = pow(2.718281828459,pow_wf)
wf = math.exp(pow_wf) #Compute wind-factor
print("Initial Spread Index Index 1 wf=",wf)

m = 1.0 #Water content in fine fuel after the drainage ???
buffer_var1 = 91.9*math.exp((-0.1386*m))
buffer_var2 = pow(m,5.31)
buffer_var3 = pow(10,7)*4.93
ffh = buffer_var1 * (1+(buffer_var2/buffer_var3)) #Compute Fine fuel humidity factor

print("Initial Spread Index Index 1 ffh=",ffh)

R = 0.208*wf*ffh #Index 1

print("Initial Spread Index Index 1 R=",R)
buffer_R = int(R)
if buffer_R==0 | buffer_R==1:
    print("Ниска степен на разпространение на пожар")
elif buffer_R>=2 & buffer_R<= 10:
    print("Висока степен от разпространение на пожар")
elif buffer_R>10:
    print("Изключително бърз темп на разпространение на пожари")


##################################################################################
#Buildup Index (BUI)
#Index 2
# U - build up index (BUI)
# P - DMC
# D - DC



##################################################################################
#Fire Weather Index (FWI)
#Index 3
# f(D) - duff humidity factor
# R - initial spread index (ISI)
# U - build up index (BUI)
# B - FWI (intermediate form)
# S - FWI (form final)



##################################################################################
# Finish Resultats
#   Very low - (0 - 1)
#   Low - (2 - 4)
#   Moderate (5 - 8)
#   High (9 - 16)
#   Very High (17-29)
#   Extreme (30+)
    


print("Fire Risk is")
S = 0
if S <= 1:
    print("FWI=",S)
    print("Very Low Risk")
elif (S>1) & (S<=4):
    print("FWI=",S)
    print("Low")
elif (S>4) & (S<=8):
    print("FWI=",S)
    print("Moderate")
elif (S>8) & (S<=16):
    print("FWI=",S)
    print("High")
elif (S>16) & (S<=29):
    print("FWI=",S)
    print("Very High")
else:
    print("FWI=",S)
    print("Extreme")

#
