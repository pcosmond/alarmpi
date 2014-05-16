cd /home/pi/Dropbox-Uploader
./dropbox_uploader.sh upload /home/pi/wifilog.log /rtalog/wifilog.log 
./dropbox_uploader.sh upload /home/log.txt /rtalog/log.txt
./dropbox_uploader.sh upload /home/pi/crontab.log /rtalog/crontab.log
#./dropbox_uploader.sh upload /home/pi/emailtst.py /rtalog/emailtst.py
#./dropbox_uploader.sh upload /home/pi/WiFi_Check /rtalog/WiFi_Check
#./dropbox_uploader.sh upload /home/pi/upload.sh /rtalog/upload.sh
#./dropbox_uploader.sh upload /var/log/cron.log /rtalog/cron.log
#./dropbox_uploader.sh upload /home/xj2alarm.py /rtalog/xj2alarm.py
#./dropbox_uploader.sh upload /home/pi/crontab.txt /rtalog/crontab.txt
sudo rm /home/pi/wifilog.log
sudo rm /home/log.txt
sudo rm /home/pi/crontab.log

