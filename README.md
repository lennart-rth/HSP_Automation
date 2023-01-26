# HSP-booking-automation
An Cronjob automation that automaticly books your sport courses for the Hochschulsport Hamburg. This only works in combination with the HSP "Ab zum Sport Card".

1. It runs 5 min. after the course has started and books for next week.
2. Requires Firefox´s or Chromes geckodriver in bash etc
3. Logs and Errors can be found in `executions.txt`. Crontab output is found in `crontab_log.txt`. 

## Installation
1. `python3 -m venv venv`
2. `source venv/bin/activate`
3. `pip3 install -r requirements.txt`
4. get geckodriver for your OS from here: https://github.com/mozilla/geckodriver/releases. To run the script on Raspberry Pi you may have to use Chromes Selenium Driver (`sudo apt-get install chromium-chromedriver` or `sudo apt-get install chromium-browser`).

### User specific setup
1. Make file called `settings.ini` and write:\
    <code>[Your Name]\
    Sport=[url_to_sport_website_with_booking_button,XPATH_to_booking_button]</code>\
     <em><strong>!!! Change "Your Name" and "Sport"-Value accordingly</strong></em>
2. Make file called `.env` with your credentials:\
<code>EMAIL={"Name":"name@email.com"}\
PASSWORD={"Name":"your_secret_passwd"}</code>\
 <em><strong>!!! Change your Name accordingly</strong></em>
\
*Note: These Passwords get saved as envoirenemt Variables and will not be seen by anyone. As long as you keep your `.env` file secret.*

## Run the automation
Make a cronjob with the command:\
 `35 19 * * 1 sh ~/HSP_Automation/run_booking.sh "Sport" "Your Name"`\
 <em><strong>!!! Change "Your Name" and "Sport"-Value and Crontab-Timing accordingly</strong></em>

