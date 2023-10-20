from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.options import Options

from time import sleep
import sys, os
from datetime import datetime
import logging
import configparser
import dotenv
import requests

from post_event import add_to_calendar

dotenv.load_dotenv()

config = configparser.ConfigParser()
config.read('settings.ini')

formatter = logging.Formatter('%(asctime)s %(message)s')

def log_to_file(filename,content):
    with open(filename,"a")as f:
        f.write(str(datetime.today())+content)

def log_result(filename,content):
    with open(filename,"a")as f:
        f.write(str(content))

options = Options()
#options.headless = True
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

returnValue = ""

def book(url, Xpath, email, passwd, user, courseNr):
    response = None
    select_course(url,Xpath, user, courseNr)
    sleep(1)
    bookable = select_free_training()
    if bookable:
        sleep(1)
        login(email,passwd, user, courseNr)
        sleep(1)
        response = confirm(user, courseNr)
    else:
        log_to_file("executions.txt",f"{datetime.today()} - Kein freier Termin zum Buchen des Kurses verfuegbar\n")
        send_notification(build_error_message(courseNr, user, f"{datetime.today().strftime('%a %H:%M')} - Kein freier Termin zum Buchen des Kurses verfuegbar"))
    #sleep(1)
    #evaluate_success()
    return response

def select_course(url,Xpath, user, courseNr):
    driver.get(url)         #url zu der Webseite des Sport
    if driver.find_element(By.XPATH, Xpath).get_attribute("value") ==  "ausgebucht":
        log_to_file("executions.txt",f"{datetime.today()} - Kurs ist schon ausgebucht!\n")
        send_notification(build_error_message(courseNr, user, f"{datetime.today().strftime('%a %H:%M')} - Kurs ist schon ausgebucht!"))
        return False
    driver.find_element(By.XPATH, Xpath).click()            #bei Kurs auf "vormerken" klicken
    driver.switch_to.window(driver.window_handles[-1])      #zum neuen tab wechseln
    return True

def select_free_training():     #einzelden termin buchen wenn er buchbar ist
    global returnValue
    table = driver.find_element(By.XPATH, "//html/body/form/div/div[2]/div/div[2]")
    success = False
    for row in table.find_elements(By.CSS_SELECTOR, "div.bs_form_row"):
        try:
            booking_btn = row.find_element(By.XPATH, ".//label/div[2]/input")
            date = row.find_element(By.XPATH, ".//label/div[1]/div[2]").text        #the date of the booked course
            time = row.find_element(By.XPATH, ".//label/div[1]/div[3]").text        #and time -//-
            courseName = driver.find_element(By.XPATH,'//*[@id="bs_ag_name"]').text
            booking_btn.click()         #if the table element has a booking-btn then click it

            start = date + " " + time.split("-")[0].replace(".",":")
            end = date + " " + time.split("-")[1].replace(".",":")
            returnValue = start + "," + end + "," + courseName
            success = True
            break
        except:
            None
    return success

def login(email, passwd, user, courseNr):
    try:
        email_field_path = "//html/body/form/div/div[2]/div[1]/div[2]/div[2]/input"
        passwd_field_path = "//html/body/form/div/div[2]/div[1]/div[3]/div[2]/input"

        driver.find_element(By.XPATH, '//*[@id="bs_pw_anmlink"]').click()       #expands the login email/passwd fields
        sleep(1)
        email_field = driver.find_element(By.XPATH, email_field_path)           #fill in email
        email_field.send_keys(email)

        passwd_field = driver.find_element(By.XPATH, passwd_field_path)         #fill in passwd
        passwd_field.send_keys(passwd)

        driver.find_element(By.XPATH, '//html/body/form/div/div[2]/div[1]/div[5]/div[1]/div[2]/input').click()      #bestätigen
    except Exception as e:
        send_notification(build_error_message(courseNr,user, str(e)))
        raise

def confirm(user, courseNr):
    try:
        agb_field_path = "//html/body/form/div/div[3]/div[2]/label/input"
        verbindlich_buchen_field = "//html/body/form/div/div[3]/div[1]/div[2]/input"

        agb_field = driver.find_element(By.XPATH, agb_field_path)       #check agb box
        agb_field.click()

        sleep(5)
        driver.find_element(By.XPATH, "//*[@id='bs_submit']").click()      #weiter zu buchen clicken

        driver.find_element(By.XPATH, verbindlich_buchen_field).click()      #verbindlich buchen klicken

        log_result("booked.txt",f"{returnValue}, {courseNr}, {user};\n")
        log_to_file("executions.txt",f"{datetime.today()} - {courseNr} - {user} - crontab executed successfully\n")
        send_notification(f"Succesfully booked {courseNr} for {user} at {datetime.today().strftime('%a %H:%M')}!")

    except Exception as e:
        send_notification(build_error_message(courseNr,user, str(e)))
        raise

    #driver.switch_to.window(driver.window_handles[-1])      #tab wechseln
    return {'name':user,'courseID':returnValue.split(",")[2], 'start': returnValue.split(",")[0], 'end': returnValue.split(",")[1]}

def evaluate_success():
    success = driver.find_element(By.XPATH, "//html/body/div/div[2]/div[1]/span[1]").text       #if this text is Bestätigung the booking was succesfull 

    if success == "Bestätigung":
        print(returnValue)
    else:
        print("Error: 'Booking not succesfull.'")

def send_notification(message):
    id = int(os.environ.get('TELEGRAMID'))
    header={
        "chat_id": id,
        "text":message,
    }
    response = requests.post(f"https://api.telegram.org/{os.environ.get('TELEGRAMTOKEN')}/"+"sendMessage", json=header)

def build_error_message(courseNr, user, msg):
    return f"Error while booking {courseNr} for {user}!\nMessage: {msg}"

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        log_to_file("executions.txt","No parameter specified\n")
        send_notification("No parameter specified")
    else:
        courseNr = sys.argv[1]
        user = sys.argv[2]

        course = eval(config[user][courseNr])
        emails = eval(os.environ.get('EMAIL'))
        passwords = eval(os.environ.get('PASSWORD'))

        response = book(course[0], course[1], emails[user], passwords[user], user, courseNr)
        response = {**response, **{"location":course[2]}}

        if eval(os.environ.get('CALID'))[user]:
            add_to_calendar(response)
        else:
            print("No Google calender integrated. Just booking without creating a event.")
            send_notification(build_error_message(courseNr,user,"No Google calender integrated. Just booking without creating a event."))

        driver.quit()
