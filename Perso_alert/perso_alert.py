from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import requests

options = Options()
# options.headless = True
options.add_argument('--headless')
# options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

url = "https://serviceportal.hamburg.de/HamburgGateway/FVP/FV/bezirke/passda/?sid=110"
telegram_url = f"https://api.telegram.org/bot6263589162:AAGzUkOG5KfHJn47wrfReI593SW-qIHQo1Q/"
serien_nr = "L1TC43YVG5"
birth = "04.08.2002"

driver.get(url)
driver.find_element(By.XPATH, "//*[@id='GatewayMaster_ContentSection_wuc_01_Query_rblAusweisArt_0']").click()
driver.find_element(By.XPATH, "//*[@id='GatewayMaster_ContentSection_wuc_01_Query_txtSeriennummer']").send_keys(serien_nr)
driver.find_element(By.XPATH, "//*[@id='GatewayMaster_ContentSection_wuc_01_Query_txtGebDat']").send_keys(birth)
driver.find_element(By.XPATH, "//*[@id='GatewayMaster_ContentSection_wuc_01_Query_btnWeiter']").click()
status = driver.find_element(By.XPATH, "//*[@id='GatewayMaster_ContentSection_wuc_02_Response_lblStatus2']").text

if "Dokument eingegangen" in status:
    header={
            "chat_id":"2049676863",
            "text":"Dein Perso ist jetzt abholbereit!\nMach einen Termin unter https://www.hamburg.de/behoerdenfinder/info/11882273/n0/",
        }
    response = requests.post(telegram_url+"sendMessage", json=header)

