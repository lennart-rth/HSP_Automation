from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import dotenv
import time
import os
from os import system
options = Options()
options.headless = True
# options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

def _eq(a,b):
    return a==b

class StineAlaram():
    def __init__(self,url,) -> None:
        self.url = url
        # driver.execute_script(f"window.open('about:blank', '{self.name}');")

        dotenv.load_dotenv()
        self.stine_nr = os.environ.get("STINENR")
        self.stine_passwd = os.environ.get("STINEPASSWD")
        

    def get_to_coursepage(self):
        # driver.switch_to.window(f"{self.name}")
        driver.get(self.url)
        time.sleep(2)
        driver.find_element(By.XPATH, "//*[@id='logIn_btn']").click()
        driver.find_element(By.XPATH, "//*[@id='Username']").send_keys(self.stine_nr)
        driver.find_element(By.XPATH, "//*[@id='Password']").send_keys(self.stine_passwd)
        driver.find_element(By.XPATH, "//html/body/div[2]/div/div[2]/div/div/div[2]/form/fieldset/div[4]/button[1]").click()    #login click
        time.sleep(2)
        driver.find_element(By.XPATH, "//html/body/div[3]/div[2]/div[5]/ul/li[5]/a").click()        #studium click
        time.sleep(2)
        driver.find_element(By.XPATH, "//html/body/div[3]/div[2]/div[5]/ul/li[5]/ul/li[1]/ul/li[1]/a").click()        #Anmeldung click
        time.sleep(2)
        driver.find_element(By.XPATH, "//html/body/div[3]/div[3]/div[2]/div[3]/ul/li[4]/a").click()        #Wahlplficht click
        time.sleep(2)
        return self.url
   
    def isCourseFree(self,xpath,comparator,compare_againts):
        # driver.switch_to.window(f"{self.name}")
        driver.refresh()
        text = driver.find_element(By.XPATH, xpath).text
        capacity = text.split("\n")[1]
        current = int(capacity.split("|")[1])
        limit = int(capacity.split("|")[0])
        if compare_againts:
            return comparator(current,compare_againts)
        else:
            return comparator(current,limit)
        