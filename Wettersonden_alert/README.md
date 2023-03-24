# Wettersonden-alert
Predict Wettersonden in the area of Hamburg and send a Email to your account if a Wettersonde lands at your home location.


"Wettersonden-alert.py" is obsolete since the originale website Wetterson.de is down.
New script called "wettersonden-alert_V.2.py" interacts with script "daily_update.py".

If the script from version two is executed in the morning, it predicts the daily ballon starts for the day.
If it is executed a second or third time on that day it tries to match current ballons in the air with the start locations of the predicted flights. If the positions match, it links the actual flight with the prediction from the morning and sends a second email, that the Sonde is actually on its way.
Only works when the second or third execution is roughly at the same Time as the scheduled launch time.
Since the launch Times are very inconsistent and differ from day to day and between the launch facilities the script is very inaccurate.


Script three only predicts the wettersonden flights with this API "http://astrohardy.de/radiosonde/predictapi.html" and checks if the landing point is in the home area. If so a reminder Email is send.


predicted.py is a command line gui for the Api to manualy query predictions. Its possible to change home position and date of prediction.


In history.txt: All predicitons are saved so a debug and evaluation is easy. history.txt is deleted every monday so it contains the predictions of the week.


Usefull Links:


Predictions:

https://predict.sondehub.org/

http://astrohardy.de/radiosonde/predictapi.html

http://weather.uwyo.edu/upperair/balloon_traj.html


Tracking:

http://map.openwx.de/

https://s1.radiosondy.info/index.php?

https://tracker.sondehub.org/?sondehub=1#!mt=osm&mz=8&qm=12_hours&mc=53.64094,9.96844&q=RS_*;*chase


Database with all active Ballons:

https://spacenear.us/tracker/datanew.php?mode=1hour&type=positions&format=json&max_positions=5&position_id=0&vehicles=RS_*;*chase

