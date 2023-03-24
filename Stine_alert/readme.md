# Stine_Alert_System

A simple reuest based Python Telegram-bot server to get notified if a University course is available to book. Can handle multi user as well as multi course alerts simultaneously.

For a even simpler Script without multi-user and telegram implementation, take a look at the "simple" branch.

## Server startup and dispose
1. Activate venv by `source venv/bin/activate`
2. Run `nohup python PiperEABot.py` to start the server, ignoring hangup signals. 
3. To stop the Server find PID of Python Process and the Chromium Driver by `ps -A` and kill them by `kill PID`

## Caveats
1. This purely relies on the STiNE Webiste.
2. Can only check for multiple courses that are on the same stine Page (eg. only Wahlpflicht or onlx Freier Wahlbereich)

## Help Page
1. Edit a Alert for a specific course globally (for all users subscribed to the bot):\
    1. Use /set_alert and append the arguments the_course_id, comparator_func, value only seperated by spaces.
    2. The value can be any integer or None if sit should be compared to the max limit of the course.
2. Set a notification for a aspecific Course for your Device:
   1. Use /set_notification  and append the arguments course_id, True or False only seperated by spaces.
3. see the status of the alerts:
    1. Returns a list of all courses available to book and each ids that are subscribed to the course.

5. Use /update_rate value_in_seconds to set the new rate in which the stine site is refreshed.

6. The course_ids that are currently available are: ...

7. The comparator_funcs that are currently available are:
    1. _eq for equals
    2. _neq for not equals
    3. _ge for greater than
    4. _le for less than

8. The values to compare againts are Integer or None.
