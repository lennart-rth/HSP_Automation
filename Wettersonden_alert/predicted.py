from datetime import datetime
import requests
import json
import math

now = datetime.now()
curdate = now.strftime("%H:%M %d.%m.%Y")
day = now.weekday()
today = now.strftime("%Y-%m-%dT")
intoday = input("enter the date from ehich you want teh predictions (format: Year-Month-Day e.g.(2021-03-04))")
today = intoday+"T"
today.replace(" ", "")
homepos = input("enter Koordinates of the region the flights schould land in: (default is Hamburg (53.551228,9.890442))")
homekoord = [53.551228,9.890442]
homekoord = homepos.split(",")
if len(homekoord) !=2:
    print("your input is invalid! Default is used!")
    homekoord = [53.551228,9.890442]
print("your query is for:",today,"at",homekoord)

data = [
["Schleswig",[5.51,10.27,31308],54.527231,9.548441],
["Sasel",[5.11,10.43,24064],53.649111,10.110911],
["Norderney",[5.33,9.83,32289],53.712111,7.151811],
["Bergen",[5.01,13.06,33511],52.815411,9.924511]]

predicitons = []
landings = []
notlandins = []

for facilities in data:
    url6 = "http://predict.cusf.co.uk/api/v1/?launch_latitude="+str(facilities[2])+"&launch_longitude="+str(facilities[3])+"&launch_altitude=20&launch_datetime="+str(today)+"05:00:00Z&ascent_rate="+str(facilities[1][0])+"&burst_altitude="+str(facilities[1][2])+"&descent_rate="+str(facilities[1][1])
    url12 = "http://predict.cusf.co.uk/api/v1/?launch_latitude="+str(facilities[2])+"&launch_longitude="+str(facilities[3])+"&launch_altitude=20&launch_datetime="+str(today)+"11:00:00Z&ascent_rate="+str(facilities[1][0])+"&burst_altitude="+str(facilities[1][2])+"&descent_rate="+str(facilities[1][1])
    url18 = "http://predict.cusf.co.uk/api/v1/?launch_latitude="+str(facilities[2])+"&launch_longitude="+str(facilities[3])+"&launch_altitude=20&launch_datetime="+str(today)+"17:00:00Z&ascent_rate="+str(facilities[1][0])+"&burst_altitude="+str(facilities[1][2])+"&descent_rate="+str(facilities[1][1])
    urls = [url6,url12,url18]

    if facilities[0] == "Sasel":
        if day == 2 or day == 3:    #wenn Mi oder Do ist dann dartet in Sasel eine Sonde
            try:
                response = requests.get(url12)
            except:
                print("error for Sasel")
            data = json.loads(response.text)
            lastPoint = []
            for x, points in enumerate(data["prediction"][1]["trajectory"]):
                lastPoint = [points["datetime"],points["latitude"],points["longitude"],points["altitude"]]
            predicitons.append([facilities[0],data["request"]["launch_datetime"],lastPoint[0],lastPoint[1],lastPoint[2],lastPoint[3]])

    if facilities[0] == "Schleswig":
        try:
            response = requests.get(url12)
        except:
            print("error for Schleswig")
        data = json.loads(response.text)
        lastPoint = []
        for x, points in enumerate(data["prediction"][1]["trajectory"]):
            lastPoint = [points["datetime"],points["latitude"],points["longitude"],points["altitude"]]
        predicitons.append([facilities[0],data["request"]["launch_datetime"],lastPoint[0],lastPoint[1],lastPoint[2],lastPoint[3]])


    if facilities[0] == "Norderney" or facilities[0] == "Bergen":
        for i in range(0,3):
            try:
                response = requests.get(url[i])
            except:
                print("error for Norderney or Bergen")
            data = json.loads(response.text)
            lastPoint = []
            for x, points in enumerate(data["prediction"][1]["trajectory"]):
                lastPoint = [points["datetime"],points["latitude"],points["longitude"],points["altitude"]]
            predicitons.append([facilities[0],data["request"]["launch_datetime"],lastPoint[0],lastPoint[1],lastPoint[2],lastPoint[3]])

for fligth in predicitons:
    radius = math.sqrt(math.pow((fligth[3]-homekoord[0]),2)+math.pow((fligth[4]-homekoord[1]),2))
    if radius <= 0.6:
        landings.append(fligth)
    else:
        notlandins.append(fligth)

print("""\
Subject: Eine Wettersonde ist gestartet! --automatisierte Benachrichtigung--

Folgende Sonden sind gestartet und werden in der Naehe von Habmburg landen:
""")

print("Report from:")
print(str(intoday))
print("Fligths that land in the given Region:")
if landings:
    linex = "============="
    for ziel in landings:
        line = "-----Launch facility: "+str(ziel[0])+"-----"
        linea = "Start Time: "+str(int(ziel[1][11:13])+1)+ "UHR"
        lineb = "ETA: "+str(int(ziel[2][11:13])+1)+":"+str(ziel[2][14:19])
        linec = "Landing Site: "+str(round(ziel[3],6))+"N "+str(round(ziel[4],6))+"O "
        lined = "last heigth: "+str(round(ziel[5],6))
        print('\n')
        print(line+ '\n')
        print(linea+ '\n')
        print(lineb+ '\n')
        print(linec+ '\n')
        print(lined+ '\n')
        print(linex+ '\n')
    print('\n')
    print('\n')
    print(linex+ '\n')
else:
    print("There are no landings in the given region")
print("")

print("Fligths that dont land in the given Region:")
if notlandins:
    linex = "============="
    for ziel in notlandins:
        line = "-----Launch facility: "+str(ziel[0])+"-----"
        linea = "Start Time: "+str(int(ziel[1][11:13])+1)+ "UHR"
        lineb = "ETA: "+str(int(ziel[2][11:13])+1)+":"+str(ziel[2][14:19])
        linec = "Landing Site: "+str(round(ziel[3],6))+"N "+str(round(ziel[4],6))+"O "
        lined = "last heigth: "+str(round(ziel[5],6))
        print('\n')
        print(line+ '\n')
        print(linea+ '\n')
        print(lineb+ '\n')
        print(linec+ '\n')
        print(lined+ '\n')
        print(linex+ '\n')
    print('\n')
    print('\n')
    print(linex+ '\n')
else:
    print("There are no landings outside the given region")
