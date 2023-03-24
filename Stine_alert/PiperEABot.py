import requests
import dotenv
import os
import threading
import json

from StineAlaramSystem import StineAlaram

class PiperEABot():
    def __init__(self) -> None:
        
        dotenv.load_dotenv()

        self.booking_url = "https://stine.uni-hamburg.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=EXTERNALPAGES&ARGUMENTS=-N000000000000001,-N000265,-Astartseite"
        self.stine_alarme = {}

        self.to_check = json.loads(os.environ.get("TOCHECK"))
        self.settings = {}
        for course in self.to_check.keys(): #populate the settings dict conatining the comparator a value to comparte againsta nd th elidt of user that want to be notified for each course
            self.settings[course] = [self._le,None,[]]  #comparator function used, value to compare against and List of user to be notified if compaarator function is true
        
        self.stine_alarm = StineAlaram(self.booking_url)
        self.stine_alarm.get_to_coursepage()

        self.TOKEN = os.environ.get("TELEGRAM_TOKEN")
        self.allowed_users = json.loads(os.environ.get("ALLOWEDUSERS"))     #list of telegram ids of all users that are allowed to chat with the bot
        self.allowed_users = [int(i) for i in self.allowed_users]

        self.url = f"https://api.telegram.org/bot{self.TOKEN}/"
        self.next_update_id = 0
        self.BOT_WAIT_SECONDS = 5
        self.STINE_WAIT_SECONDS = 2

        self._update()
        self.fetch_course()

    def sendMessage(self,chat_id,text):
        header={
            "chat_id":chat_id,
            "text":text,
        }
        response = requests.post(self.url+"sendMessage", json=header)
        return response.json()

    def _getUpdates(self,header):
        response = requests.post(self.url+"getUpdates", json=header)
        return response.json()


    def _processCommand(self,command):
        if command[0] == "/status":
            message = ""
            for (key,value) in self.settings.items():
                message += f"{key} with {value[0].__name__} on {value[1]} for {value[2]}\n"
            self.sendMessage(command[1],message)
        elif command[0] == ("/help"):
            message = f"1. Edit a Alert for a specific course globally (for all users subscribed to the bot):\n   Use /set_alert and append the arguments the_course_id, comparator_func, value only seperated by spaces.\n   The value can be any integer or None if sit should be compared to the max limit of the course.\n\n2. Set a notification for a aspecific Course for your Device:\n    Use /set_notification  and append the arguments course_id, True or False only seperated by spaces. \n\n3. see the status of the alerts:\n   Returns a list of all courses available to book and each ids that are subscribed to the course. \n\n4. Use /update_rate value_in_seconds to set the new rate in which the stine site is refreshed.\n\nThe course_ids that are currently available are:\n    {self.settings.keys()}\n\nThe comparator_funcs that are currently available are:\n    1. _eq for equals\n    2. _neq for not equals\n    3. _ge for greater than\n   4. _le for less than\n\nThe values to compare againts are Integer or None."
            self.sendMessage(command[1],message)
        elif command[0].startswith("/update_rate"):
            splited_command = command[0].split(" ")
            if len(splited_command) > 1:
                rate = splited_command[1]
                self.STINE_WAIT_SECONDS = int(rate)
                self.sendMessage(command[1],f"Update rate succesfully set to {rate} seconds.")
            else:
                self.sendMessage(command[1],"Your command was wrong! You have to append a rate Arguments to the command /update_rate.\nRate must be a single value like 3.")
        elif command[0].startswith("/set_alert"):
            #schema: command "command courseID comarator function value if not None"
            splited_command = command[0].split(" ")
            if len(splited_command) > 1:
                if splited_command[1] in self.settings.keys():
                    if splited_command[2] in ["_eq","_neq","_ge","_le"]:
                        new_comp = self.get_comp(splited_command[2])
                        self.settings[splited_command[1]][0] = new_comp     #change the comparator func for that course
                        if splited_command[3] == "None":
                            self.settings[splited_command[1]][1] = None  #change the value to compare against to None. The value will be ignored and instead comared to the max limit of that course.
                        else:
                            self.settings[splited_command[1]][1] = int(splited_command[3])  #change the value to compare against for that course
                        self.sendMessage(command[1],f"The settings for {splited_command[1]} are saved!")
                    else:
                        self.sendMessage(command[1],"Your comparator function was wrong! Choose one: _eq, _neq, _ge, _le")
                else:
                    self.sendMessage(command[1],"Your command was wrong! The Course_id was not found in the list.")
            else:
                self.sendMessage(command[1],"Your command was wrong! You have to append Arguments to the command /set_alert.")
        elif command[0].startswith("/set_notification"):
            #schema: "command courseID True/False"
            splited_command = command[0].split(" ")
            if len(splited_command) > 1:
                if splited_command[1] in self.settings.keys() and splited_command[2] == "True":
                    self.settings[splited_command[1]][2].append(command[1])     #add new chat_id to the list of users taht want to be notified for that Course
                    self.sendMessage(command[1],f"The notification for {splited_command[1]} is now turned on!")
                elif splited_command[1] in self.settings.keys() and splited_command[2] == "False":
                    self.settings[splited_command[1]][2].remove(command[1])     #remove new chat_id to the list of users taht want to be notified for that Cours
                    self.sendMessage(command[1],f"The notification for {splited_command[1]} is now turned off!")
                else:
                    if splited_command[1] not in self.settings.keys():
                        self.sendMessage(command[1],"Your command was wrong! The Course_id was not found in the list.")
                    else:
                        self.sendMessage(command[1],"Your command was wrong! Acceptet scheme is '/set_notification course_id True/False'")
            else:
                self.sendMessage(command[1],"Your command was wrong! You have to append Arguments to the command /set_notification.")
            

    def _update(self):
        header = {
        "offset": self.next_update_id,
        }
        data = self._getUpdates(header)
        try:
            if data["result"]:
                result = data["result"]
                self.next_update_id = result[-1]["update_id"] + 1

                if "entities" in result[-1]["message"] and result[-1]["message"]["from"]["id"] in self.allowed_users:
                    # if result[0]["message"]["entities"][0]["type"] == "bot_command":
                    # SCHEMA: received_command = (text,chat_id)
                    received_command = (result[-1]["message"]["text"],result[-1]["message"]["chat"]["id"])
                    self._processCommand(received_command)
        except:pass

        threading.Timer(self.BOT_WAIT_SECONDS, self._update).start()
    
    def fetch_course(self):
        for key,val in self.settings.items():
            if len(val[2]) > 0:
                if self.stine_alarm.isCourseFree(self.to_check[key],val[0],val[1]):
                    for chat_id in val[2]:
                        self.sendMessage(chat_id,f"{key} ist jetzt buchbar! \n Here:{self.booking_url}")
        threading.Timer(self.STINE_WAIT_SECONDS, self.fetch_course).start()

    def _eq(self,a,b):
        return a==b
    def _neq(self,a,b):
        return a!=b
    def _le(self,a,b):
        return a<b
    def _ge(self,a,b):
        return a>b
    
    def get_comp(self,name):
        if name == "_eq":
            return self._eq
        elif name == "_neq":
            return self._neq
        elif name == "_le":
            return self._le
        elif name == "_ge":
            return self._ge

BV = PiperEABot()