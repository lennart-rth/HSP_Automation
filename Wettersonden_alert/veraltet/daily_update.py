import json
import requests
import smtplib, ssl
from datetime import datetime

#home = [9.50,10.30,53.40,53.80]
home = [8.60,11.05,52.40,54.70]        #a bigger radius for testing
#print(home)
hit = []

def daily_update(sending):
    print("ruuun",sending)
    now = datetime.now()
    # dd/mm/YY H:M:S
    today = now.strftime("%d/%m/%Y %H:%M:%S")

    jetzt = datetime.now()
    # dd/mm/YY H:M:S
    todaydate = now.strftime("%Y-%m-%d")

    inRegion = []

    url =["http://happysat.nl/predict/bergen_predictions.json",
    "http://happysat.nl/predict/sasel_predictions.json",
    "http://happysat.nl/predict/schleswig_predictions.json",
    "http://happysat.nl/predict/meppen_predictions.json",
    "http://happysat.nl/predict/norderney_predictions.json",
    "http://happysat.nl/predict/pinneberg_predictions.json"]

    for i ,u in enumerate(url):

        response = requests.get(u)
        data = json.loads(response.text)
        site = data["site"]
        inRegion.append([site])
        predictions = data["predictions"]
        pred = []
        for a in predictions:
            pred.append(a)
        #------------flatten the JSON-----------------

        flat = {}
        def flatten(x, name=''):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + '_')
            elif type(x) is list:
                k = 0
                for a in x:
                    flatten(a, name + str(k) + '_')
                    k += 1
            else:
                flat[name[:-1]] = x

        flatten(data)
        #print(flat)
        #-----------find the landing point of each prediction----------------
        landing = []
        for a in pred:
            searchlast = True
            cnt = 0
            while searchlast:
                try:
                    flat["predictions_"+str(a)+"_path_"+str(cnt)+"_0"]
                except:
                    name = flat["predictions_"+str(a)+"_timestamp"]
                    x = flat["predictions_"+str(a)+"_path_"+str(cnt-1)+"_0"]
                    y = flat["predictions_"+str(a)+"_path_"+str(cnt-1)+"_1"]
                    stx = flat["launch_lat"]
                    sty =flat["launch_lon"]
                    landing.append([name,x,y,stx,sty])
                    searchlast = False
                cnt += 1

         # ------------------------filter landings by home position------------------------
        #print(landing)
        for land in landing:
            if (land[2]>= home[0] and land[2]<= home[1]) and (land[1]>= home[2] and land[1]<= home[3]):
                inRegion[i].append(land)

    #--------filter hit data---only tody is needed
    startnow = []
    for up in inRegion:
        if len(up)>1:
            if up[1][0][0:10] == todaydate:
                startnow.append(up)



    # startnow = [
    # ['Meppen', ['2021-03-03 13:45:00', 52.6513, 8.86533, 52.715, 7.319], ['2021-03-03 16:45:00', 52.5349, 8.9602, 52.715, 7.319], ['2021-03-03 19:45:00', 52.6053, 8.88939, 52.715, 7.319], ['2021-03-03 22:45:00', 52.6588, 8.91566, 52.715, 7.319],
    # ['2021-03-04 01:45:00', 52.6451, 8.92942, 52.715, 7.319], ['2021-03-04 04:45:00', 52.7022, 8.84129, 52.715, 7.319], ['2021-03-04 07:45:00', 52.603, 8.65856, 52.715, 7.319]],
    # ['Norderney', ['2021-03-03 22:45:00', 53.4661, 8.94586, 53.712, 7.1518], ['2021-03-04 10:45:00', 53.2531, 8.97387, 53.712, 7.1518],
    # ['2021-03-04 22:45:00', 52.8579, 9.05899, 53.712, 7.1518], ['2021-03-06 22:45:00', 53.0332, 8.70216, 53.712, 7.1518], ['2021-03-07 10:45:00', 53.1069, 8.78087, 53.712, 7.1518], ['2021-03-09 10:45:00', 53.325, 9.00226, 53.712, 7.1518],
    # ['2021-03-09 22:45:00', 52.7351, 9.74945, 53.712, 7.1518], ['2021-03-10 10:45:00', 52.8111, 10.9237, 53.712, 7.1518], ['2021-03-11 10:45:00', 53.6799, 9.30632, 53.712, 7.1518]]]
    # # #startnow = [['Bergen'], ['Sasel'], ['Schleswig'], ['Meppen'], ['Norderney'], ['Pinneberg']]

    import pickle
    predictionfile = open("predictions", "wb")
    pickle.dump(startnow, predictionfile)

    #---------display sonden inside home-area-----------------

    report = open("reportas.txt", "w")
    report.write("""\
Subject: Eine Sonde landet bald! --automatisierte Benachrichtigung--

Dies ist der automatisierte Report fuer Wettersonnden in der Umgebung von Hamburg.


""")

    linex = "============="
    line = "Bericht vom:  " + today
    report.write(line+ '\n')

    send = False
    for start in startnow:
        if len(start) > 1:
            send = True
            linea = "---------Launch facility: "+str(start[0])+"---------"
            report.write('\n')
            report.write(linea+ '\n')
            report.write('\n')
            for i in range(1,len(start)):
                lineb = "Start Time: "+str(start[i][0])
                linec = "Koordinates: "+str(start[i][1])+"N"+str(start[i][2])+"O"

                report.write(lineb+ '\n')
                report.write(linec+ '\n')
                report.write(linex+ '\n')

    report.close()

    #----------------------------send E-mail-----------------------------------

    if send and sending:
        f = open("reportas.txt", "r")

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
    return(startnow)
