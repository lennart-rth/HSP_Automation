# HSP-booking-automation
An Cronjob automation that automaticly books your sport courses for the Hochschulsport Hamburg. This only works in combination with the HSP "Ab zum Sport Card". If a google Calender is integrated, it will automaticly generate events for every booked course.

1. It runs 5 min. after the course has started and books for next week.
2. Requires Firefox´s or Chromes geckodriver in bash etc
3. Logs and Errors can be found in `executions.txt`. Raw Crontab output is found in `crontab_log.txt`. A History of all booked courses is in `booked.txt`.

## Installation
1. `python3 -m venv venv`
2. `source venv/bin/activate`
3. `pip3 install -r requirements.txt`
4. get geckodriver for your OS from here: https://github.com/mozilla/geckodriver/releases. To run the script on Raspberry Pi you may have to use Chromes Selenium Driver (`sudo apt-get install chromium-chromedriver` or `sudo apt-get install chromium-browser`).

### User specific setup
1. Make file called `settings.ini` and write:\
    <code>[<Your_Name>]\
    Sport=[<url_to_sport_website_with_booking_button>,<XPATH_to_booking_button>]</code>\
     <em><strong>!!! Change all Fields with <> accordingly</strong></em>
2. Make file called `.env` with your credentials:\
<code>EMAIL={<Name>:<name@email.com>}\
PASSWORD={<Name>:<your_secret_passwd>}</code>\
 <em><strong>!!! Change all Fields with <> accordingly</strong></em>
\
*Note: These Passwords get saved as envoirenemt Variables and will not be seen by anyone. As long as you keep your `.env` file secret.*

## Integrate Google Calendar
If you want to integrate Google Calender you have to setup a Google Service-account.
1. Folow [this](https://developers.google.com/calendar/api/quickstart/python?hl=de) to setup Google Cloud Project and [this](https://cloud.google.com/iam/docs/creating-managing-service-accounts?hl=de) to setup a service-acount.
2. Generate a Key and download ist credentials into a `credentials.json` file into the project directory.
3. Generate a new Calender and share it with your service-account. (All previleges)
4. Add the following line ionto your `.env` file:\
 `CALID={<Name>:<your_secret_calender_id>}` \
 <em>You can find your calendar Id in the setting for your calender.</em>

## Run the automation
Make a cronjob with the command:\
 `35 19 * * 1 sh ~/HSP_Automation/run_booking.sh <Sport> <Your Name>`\
 <em><strong>!!! Change "Your Name" and "Sport"-Value and Crontab-Timing accordingly</strong></em>

