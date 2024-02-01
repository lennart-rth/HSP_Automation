cd ~/HSP_Automation/
# python3 HSP-automation.py $1 $2 >> ~/HSP_Automation/crontab_log.txt
docker run --rm -w /home/pi/HSP_Automation -v $(pwd):/home/pi/HSP_Automation hspautomation python HSP-automation.py $1 $2 >> ~/HSP_Automation/crontab_log.txt