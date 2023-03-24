from datetime import datetime
import smtplib, ssl
import requests
import json
import math

now = datetime.now()
day = now.weekday()
today = now.strftime("%Y-%m-%dT")
#print(today)
data = [
["Schleswig",[5.51,10.27,31308],54.527231,9.548441],
["Sasel",[5.11,10.43,24064],53.649111,10.110911],
["Norderney",[5.33,9.83,32289],53.712111,7.151811],
["Bergen",[5.01,13.06,33511],52.815411,9.924511]]

predicitons = []
landings = []

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
    print(fligth)
    radius = math.sqrt(math.pow((fligth[3]-53.551228),2)+math.pow((fligth[4]-9.890442),2))
    if radius <= 0.6:
        landings.append(fligth)

if landings:
    print("sending email")
    report_check = open("report_check.txt", "w")
    report_check.write("""\
Subject: Eine Wettersonde ist gestartet! --automatisierte Benachrichtigung--

Folgende Sonden sind gestartet und werden in der Naehe von Habmburg landen:
""")

    linex = "============="
    for ziel in landings:
        line = "-----Launch facility: "+str(ziel[0])+"-----"
        linea = "Start Time: "+str(int(ziel[1][11:13])+1)+ "UHR"
        lineb = "ETA: "+str(int(ziel[2][11:13])+1)+":"+str(ziel[2][14:19])
        linec = "Landing Site: "+str(round(ziel[3],6))+"N "+str(round(ziel[4],6))+"O "
        lined = "last heigth: "+str(round(ziel[5],6))
        report_check.write('\n')
        report_check.write(line+ '\n')
        report_check.write(linea+ '\n')
        report_check.write(lineb+ '\n')
        report_check.write(linec+ '\n')
        report_check.write(lined+ '\n')
        report_check.write(linex+ '\n')
    report_check.write('\n')
    report_check.write('\n')
    report_check.write(linex+ '\n')
    report_check.write("""\
Linksammlung:
Tracking:
https://tracker.sondehub.org/?sondehub=1#!mt=osm&mz=8&qm=12_hours&mc=53.64094,9.96844&q=RS_*;*chase
http://map.openwx.de/
https://s1.radiosondy.info/index.php?
Vorhersagen:
https://predict.sondehub.org/
http://astrohardy.de/radiosonde/predictapi.html
http://weather.uwyo.edu/upperair/balloon_traj.html
Datenbank mit aktuell fliegenden Sonden:
https://spacenear.us/tracker/datanew.php?mode=1hour&type=positions&format=json&max_positions=5&position_id=0&vehicles=RS_*;*chase
""")
    report_check.close()

    #----------------------------send E-mail-----------------------------------

    f = open("report_check.txt", "r")

    port = 465  # For SSL
    smtp_server = "smtp.strato.de"
    sender_email = "YOUR@EMALI.COM"  # Enter your address
    receiver_email = "YOUR@EMALI.COM"  # Enter receiver address
    password = "YOUR PASSWORD"
    message = str(f.read())

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    f.close()
