# HSP-booking-automation
# !!!Do NOT publish **public**!!!

An Cronjob automation that automaticly books your sport courses. This only works for the HSP "Sport-Card".

1. It runs 1 min. after the course has started and books for next week.
2. Requires Firefox´s geckodriver in same place as the HSP-automation.py file.
3. Errors will be send per email and logged to cronjob_logs.txt in the same dir.

How to add new course:
1. make a new entry in the `courses` dictionary. <br />Format: <code>"name_to_call_by_parameter": ["url_to_website","XPATH_url_to_booking_button"]</code>
2. transfer file to IRZ folder: <br />`scp HSP-automation.py 1roth@rzssh1.informatik.uni-hamburg.de:infhome/Documents/HSP_Automation`
3. make a new entry in the crontab file (open with `crontab -e`) <br />Format: <code>* * * * * cd ~/infhome/Documents/HSP_Automation; python3 HSP-automation.py course_Name User  >> ~/infhome/Documents/HSP_Automation/crontab_log.txt</code>
