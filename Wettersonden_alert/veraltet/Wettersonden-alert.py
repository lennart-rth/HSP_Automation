import json
import requests
import smtplib, ssl

home = [9.50,10.10,53.40,53.80]
#home = [8.60,11.05,52.40,54.70]        #a bigger radius for testing
#print(home)

response = requests.get("https://wetterson.de/getgeoj-pre.php?geoj=1")
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

#-----------find the landing point of each prediction----------------

landings = []
no = True
noo = True

x = 0
while no:
    try:
        flat["features_" + str(x) + "_geometry_geometries_1_coordinates_0_0"]
        y = 0
        noo = True
        while noo:
            try:
                flat["features_" + str(x) + "_geometry_geometries_1_coordinates_" + str(y) + "_0"]
                y += 1
            except:
                landings.append([round(flat["features_" + str(x) + "_geometry_geometries_1_coordinates_" + str(y-1) + "_0"],2),round(flat["features_" + str(x) + "_geometry_geometries_1_coordinates_" + str(y-1) + "_1"],2),x,y-1])     #save the x korrdinate of landing point
                #print(flat["features_" + str(x) + "_geometry_geometries_1_coordinates_" + str(y-1) + "_1"])     #save the y korrdinate of landing point
                noo = False

    except:
        #print("finished")
        no = False
    x += 1


# ------------------------filter landings by home position------------------------
#print(landings)
inRegion = []
for land in landings:
    if (land[0]>= home[0] and land[0]<= home[1]) and (land[1]>= home[2] and land[1]<= home[3]):
        inRegion.append(land)


#---------disply sonden inside home-area-----------------

report = open("report.txt", "w")
report.write("""\
Subject: Eine Sonde landet bald! -automatisierte Benachrichtigung-

Dies ist der automatisierte Report fuer Wettersonnden in der Umgebung von Hamburg.



""")


if len(inRegion) >= 1:
    count = 1
    for hit in inRegion:
        line = "Sonde NR.:"+str(count)
        linea = "Launch facility:"+str(flat["features_"+str(hit[2])+"_properties_id"])
        lineb = "Time on start:"+str(flat["features_"+str(hit[2])+"_properties_dtime"])
        linec = "Max. Altitude:"+str(flat["features_"+str(hit[2])+"_properties_alti"])
        lined = "Landing Koordinates:"+str(flat["features_" + str(hit[2]) + "_geometry_geometries_1_coordinates_" + str(hit[3]) + "_0"])  +","+  str(flat["features_" + str(hit[2]) + "_geometry_geometries_1_coordinates_" + str(hit[3]) + "_1"])
        linee = "========================================"
        report.write(line+ '\n')
        report.write(linea+ '\n')
        report.write(lineb+ '\n')
        report.write(linec+ '\n')
        report.write(lined+ '\n')
        report.write(linee+ '\n')
        report.write("\n")
        count +=1

    report.close()




#----------------------------send E-mail-----------------------------------

    f = open("report.txt", "r")

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
