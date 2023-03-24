import json
import requests
import smtplib, ssl
from datetime import datetime
from daily_update import daily_update
from daily_update import home

#Einstellungen
precision = 50    #ab wann soll eine sonde die aktuell gestartet ist mit einer vorhersage zu diesem zeitraum gematch werden. (größe ist der errpr berechnung dx+dy dx = aktueller pos der sonde minus pos des startplatz )
maxhöhe = 30000  #höhe bis zu der die sonde in erwägung gezogen wird. erst danach wird der Error berechnet.


now = datetime.now()
hour = now.strftime("%H")
#hour = 6
if hour == 6:
    daily_update(True)

else:
    import pickle
    predicitonfile = open ('predictions', 'rb')
    hit = pickle.load(predicitonfile)
    print(hit)
    response = requests.get("https://spacenear.us/tracker/datanew.php?mode=1hour&type=positions&format=json&max_positions=0&position_id=0&vehicles=RS_*;*chase")
    data = json.loads(response.text)

    #------------flatten the JSON-----------------

    flat = {}
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            flat[name[:-1]] = x

    flatten(data)
    #print(flat)

    #-------find relevant flights------------       die die mit den Startplätzen der Sonde übereinstimmen

    def takeSecond(elem):
        return elem[1]

    pair = []
    for launch in hit:
        if len(launch) >1:
            min = []
            for i in range(0,len(data["positions"]["position"])):
                name = flat["positions_position_"+str(i)+"_vehicle"]
                x = float(flat["positions_position_"+str(i)+"_gps_lat"])
                y = float(flat["positions_position_"+str(i)+"_gps_lon"])
                z = float(flat["positions_position_"+str(i)+"_gps_alt"])
                #print(name,x,y,z)
                if name[0:2] == "RS":
                    if z <= maxhöhe:
                        xk = launch[1][3]
                        yk = launch[1][4]
                        dx = abs(xk-x)
                        dy = abs(yk-y)
                        error = dx+dy
                        min.append([name,error])
            try:
                min.sort(key = takeSecond)
            except:
                print("fehler: Es wirde kein Minimum für diese sonde gefunden.")
            #print(min)
            pair.append([launch[0],min[0][0],launch[1][0],min[0][1]])

    print(pair)
    #------------report startet fligths that match the prediciton from before--------
    report_check = open("report_check.txt", "w")
    report_check.write("""\
Subject: Die Sonde ist gestartet! --automatisierte Benachrichtigung--

Folgende Sonden sind gestartet und werden in der Naehe von Habmburg landen.


""")

    linex = "============="
    sended = False
    for ziel in pair:
        if ziel[3] <= precision:
            sended = True
            line = "---------Launch facility: "+str(ziel[0])+"---------"
            linea = "Sonden ID: "+str(ziel[1])
            lineb = "Start Time: "+str(ziel[2])
            linec = "Error(das sie es ist): "+str(ziel[3])
            report_check.write('\n')
            report_check.write(line+ '\n')
            report_check.write(linea+ '\n')
            report_check.write(lineb+ '\n')
            report_check.write(linec+ '\n')
            report_check.write(linex+ '\n')

    report_check.close()

    #----------------------------send E-mail-----------------------------------

    if sended:
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
