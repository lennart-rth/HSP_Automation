from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from time import sleep
import sys, os
from datetime import datetime
import logging
import configparser
import dotenv

dotenv.load_dotenv()

config = configparser.ConfigParser()
config.read('settings.ini')

formatter = logging.Formatter('%(asctime)s %(message)s')

def log_to_file(filename,content):
    with open(filename,"a")as f:
        f.write(str(datetime.today())+content)

def log_result(filename,content):
    with open(filename,"a")as f:
        f.write(str(content).rstrip('\n'))

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

returnValue = ""

def book(url, Xpath, email, passwd):
    select_course(url,Xpath)
    sleep(1)
    bookable = select_free_training()
    if bookable:
        sleep(1)
        login(email,passwd)
        sleep(1)
        confirm()
    else:
        log_to_file("executions.txt",f"{datetime.today()} - Kein freier Termin zum Buchen des Kurses verfügbar.\n")
    #sleep(1)
    #evaluate_success()

def select_course(url,Xpath):
    driver.get(url)         #url zu der Webseite des Sport
    if driver.find_element(By.XPATH, Xpath).get_attribute("value") ==  "ausgebucht":
        log_to_file("executions.txt",f"{datetime.today()} - Kurs ist schon ausgebucht!\n")
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
            booking_btn.click()         #if the table element has a booking-btn then click it

            start = date + " " + time.split("-")[0].replace(".",":")
            end = date + " " + time.split("-")[1].replace(".",":")
            returnValue = start + "," + end
            success = True
            break
        except:
            None
    return success

def login(email, passwd):
    email_field_path = "//html/body/form/div/div[2]/div[1]/div[2]/div[2]/input"
    passwd_field_path = "//html/body/form/div/div[2]/div[1]/div[3]/div[2]/input"

    driver.find_element(By.XPATH, '//*[@id="bs_pw_anmlink"]').click()       #expands the login email/passwd fields
    sleep(1)
    email_field = driver.find_element(By.XPATH, email_field_path)           #fill in email
    email_field.send_keys(email)

    passwd_field = driver.find_element(By.XPATH, passwd_field_path)         #fill in passwd
    passwd_field.send_keys(passwd)

    driver.find_element(By.XPATH, '//html/body/form/div/div[2]/div[1]/div[5]/div[1]/div[2]/input').click()      #bestätigen

def confirm():
    agb_field_path = "//html/body/form/div/div[3]/div[2]/label/input"
    verbindlich_buchen_field = "//html/body/form/div/div[3]/div[1]/div[2]/input"

    agb_field = driver.find_element(By.XPATH, agb_field_path)       #check agb box
    agb_field.click()

    sleep(5)
    driver.find_element(By.XPATH, "//*[@id='bs_submit']").click()      #weiter zu buchen clicken

    driver.find_element(By.XPATH, verbindlich_buchen_field).click()      #verbindlich buchen klicken

    log_result("ical.txt",f"{returnValue}, {courseNr}, {user};")
    log_to_file("executions.txt",f"{datetime.today()} - {courseNr} - {user} - crontab executed successfully\n")

    #driver.switch_to.window(driver.window_handles[-1])      #tab wechseln

def evaluate_success():
    success = driver.find_element(By.XPATH, "//html/body/div/div[2]/div[1]/span[1]").text       #if this text is Bestätigung the booking was succesfull 

    if success == "Bestätigung":
        print(returnValue)
    else:
        print("Error: 'Booking not succesfull.'")

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        log_to_file("executions.txt","No parameter specified\n")
    else:
        courseNr = sys.argv[1]
        user = sys.argv[2]

        course = eval(config[user][courseNr])
        emails = eval(os.environ.get('EMAIL'))
        passwords = eval(os.environ.get('PASSWORD'))

        book(course[0], course[1], emails[user], passwords[user])

        driver.quit()
