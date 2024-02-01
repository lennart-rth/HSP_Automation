# Build CMD: docker build -t hspautomation .
# RUN CMD: docker run --rm -w /home/pi/HSP_Automation -v $(pwd):/home/pi/HSP_Automation hspautomation python HSP-automation.py Radfahren Lennart
# In crontab it is run with sh ~/HSP_Automation/run_booking.sh Laufen Lennart

FROM python:3.10-buster

RUN apt-get -y update
RUN apt-get install -y chromium chromium-driver

RUN pip install --upgrade pip
RUN pip install cryptography==3.3.2
RUN pip install selenium==4.8.0
RUN pip install google_api_python_client==2.74.0
RUN pip install protobuf==4.21.12
RUN pip install python-dotenv==0.21.1