from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options
from time import sleep
import sys, os
import logging
import configparser
import dotenv

dotenv.load_dotenv()

config = configparser.ConfigParser()
config.read('settings.ini')

formatter = logging.Formatter('%(asctime)s %(message)s')

def setup_logger(name, log_file, mode):
    handler = logging.FileHandler(log_file,mode=mode)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.addHandler(handler)

    return logger

exception_logger = setup_logger('Exception_Logger', 'booking_exceptions.log', 'w')

booking_logger = setup_logger('Booking_Logger', 'booking.log','a')

service = Service('./geckodriver')

options = Options()
options.add_argument("-headless")
driver = webdriver.Firefox(service=service, options=options)
returnValue = ""

def book(url, Xpath, email, passwd):
    select_course(url,Xpath)
    sleep(1)
    select_free_training()
    sleep(1)
    login(email,passwd)
    # sleep(1)
    # confirm()
    #sleep(1)
    #evaluate_success()

def select_course(url,Xpath):
    driver.get(url)         #url zu der Webseite des Sport
    driver.find_element(By.XPATH, Xpath).click()            #bei Kurs auf "vormerken" klicken
    driver.switch_to.window(driver.window_handles[-1])      #zum neuen tab wechseln

def select_free_training():     #einzelden termin buchen wenn er buchbar ist
    global returnValue
    table = driver.find_element(By.XPATH, "//html/body/form/div/div[2]/div/div[2]")
    for row in table.find_elements(By.CSS_SELECTOR, "div.bs_form_row"):
        try:
            booking_btn = row.find_element(By.XPATH, ".//label/div[2]/input")
            date = row.find_element(By.XPATH, ".//label/div[1]/div[2]").text        #the date of the booked course
            time = row.find_element(By.XPATH, ".//label/div[1]/div[3]").text        #and time -//-
            booking_btn.click()         #if the table element has a booking-btn then click it
            #04.10.2022
            #13.20-14.30
            start = date + " " + time.split("-")[0].replace(".",":")
            end = date + " " + time.split("-")[1].replace(".",":")
            returnValue = start + "," + end
            break
        except:
            None

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

    #print(returnValue)
    booking_logger.info(f"{returnValue}, {courseNr}, {user}")


    #driver.switch_to.window(driver.window_handles[-1])      #tab wechseln

def evaluate_success():
    success = driver.find_element(By.XPATH, "//html/body/div/div[2]/div[1]/span[1]").text       #if this text is Bestätigung the booking was succesfull

    if success == "Bestätigung":
        #print(returnValue)
        booking_logger.info(f"{returnValue}, {courseNr}, {user}")

    else:
        #print("Error: 'Booking not succesfull.'")
        exception_logger.exception("Exception occurred")

if __name__ == "__main__":
    # courses = {
    #     "Radfahren":["https://buchung.hochschulsport-hamburg.de/angebote/Wintersemester_2022_2023/_Triathlon.html","//html/body/div[1]/div/main/section[1]/article/div[2]/div/div/form/div[6]/div[2]/table/tbody/tr[1]/td[9]/input"],
    #     "Laufen":["https://buchung.hochschulsport-hamburg.de/angebote/Wintersemester_2022_2023/_Triathlon.html","//html/body/div[1]/div/main/section[1]/article/div[2]/div/div/form/div[5]/div[2]/table/tbody/tr/td[9]/input"],
    #     "Schwimmen_Mo":["https://buchung.hochschulsport-hamburg.de/angebote/aktueller_zeitraum/_Schwimmtechnik___Schwimmtraining.html","//html/body/div[1]/div/main/section[1]/article/div[2]/div/div/form/div[9]/div[2]/table/tbody/tr[1]/td[9]/input"],
    #     "Schwimmen_Mi":["https://buchung.hochschulsport-hamburg.de/angebote/aktueller_zeitraum/_Schwimmtechnik___Schwimmtraining.html","//html/body/div[1]/div/main/section[1]/article/div[2]/div/div/form/div[10]/div[2]/table/tbody/tr/td[9]/input"],
    #     "Schwimmen_Sa":["https://buchung.hochschulsport-hamburg.de/angebote/Wintersemester_2022_2023/_Triathlon.html","//html/body/div[1]/div/main/section[1]/article/div[2]/div/div/form/div[7]/div[2]/table/tbody/tr[2]/td[9]/input"],
    #     "HIIT": ["https://buchung.hochschulsport-hamburg.de/angebote/Wintersemester_2022_2023/_HIIT__und__Core_-_online.html","//html/body/div[1]/div/main/section[1]/article/div[2]/div/div/form/div[4]/div[2]/table/tbody/tr/td[9]/input"],
    #     "Rücken_Do": ["https://buchung.hochschulsport-hamburg.de/angebote/aktueller_zeitraum/_Rueckenfitness_-_online.html","//html/body/div[1]/div/main/section[1]/article/div[2]/div/div/form/div[5]/div[2]/table/tbody/tr/td[9]/input"],
    #     "Bauch-Rücken-Stretch": ["https://buchung.hochschulsport-hamburg.de/angebote/aktueller_zeitraum/_Bauch_Ruecken_Stretch_-_online.html","//html/body/div[1]/div/main/section[1]/article/div[2]/div/div/form/div[4]/div[2]/table/tbody/tr/td[9]/input"],
    #     "Dance-Fitness": ["https://buchung.hochschulsport-hamburg.de/angebote/aktueller_zeitraum/_Dance_Fitness_-_online.html","/html/body/div[1]/div/main/section[1]/article/div[2]/div/div/form/div[5]/div[2]/table/tbody/tr/td[9]/input"]}

    if len(sys.argv) <= 1:
        exception_logger.exception("No parameter specified")
    else:
        courseNr = sys.argv[1]
        user = sys.argv[2]
        #course = courses[courseNr]      #array mit [Url_zur_seite, XPATH_zum_Buchen_Btn]

        course = config[user][courseNr]
        emails = os.environ.get('EMAIL')
        passwords = os.environ.get('PASSWORD')

        try:
            book(course[0], course[1], emails[user], passwords[user])
        except Exception as e:
            exception_logger.exception("Exception occurred")
        finally:
            driver.quit()
