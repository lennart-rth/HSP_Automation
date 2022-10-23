# HSP-booking-automation
An Cronjob automation that automaticly books your sport courses for the Hochschulsport Hamburg. This only works for the HSP "Sport-Card".



1. It runs 1 min. after the course has started and books for next week.
2. Requires Firefox´s geckodriver in same place as the HSP-automation.py file.
3. Logs can be found in `booking.log` and exeptions in `booking_exceptions.log`. Crontab output is found in `crontab_log.txt`. 

## Installation
1. `python3 -m venv venv`
2. `source venv/bin/activate`
3.  `pip3 install -r requirements.txt`

### User specific setup
1. Make file called `settings.ini` and write:\
    <code>[Name]\
    Sport=[url_to_sport_website_with_booking_button,XPATH_to_booking_button]</code>\
     <em><strong>!!! Change your Name and Sport accordingly</strong></em>
2. Make file called `.env` with your credentials:\
<code>EMAIL={"Name":"name@email.com"}\
PASSWORD={"Name":"your_secret_passwd"}</code>\
 <em><strong>!!! Change your Name accordingly</strong></em>
\
*Note: These Passwords get saved as envoirenemt Variables and will not be seen by anyone. As long as you keep your `.env` file secret.*

## Run th automation
Make a cronjob with the command:\
 `cd /path/to/your/dir; python3 HSP-automation.py Sport Name  >> ~/infhome/Documents/HSP_Automation/crontab_log.txt`\
 <em><strong>!!! Change your Name and Sport accordingly</strong></em>

## Automatically generate calender appointments
`fetch_bokking.sh` allows to retrieve information about the last succesfull booking. You can use it to automaticly generate a calender appointement, by calling this script from a Ios Shortcuts automation.