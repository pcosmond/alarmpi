cd /home/pi/Dropbox-Uploader
./dropbox_uploader.sh upload /home/pi/wifilog.log /LJlog/wifilog.log 
./dropbox_uploader.sh upload /home/log.txt /LJlog/log.txt
./dropbox_uploader.sh upload /home/pi/crontab.log /LJlog/crontab.log
#./dropbox_uploader.sh upload /home/pi/emailtst.py /LJlog/emailtst.py
#./dropbox_uploader.sh upload /home/pi/WiFi_Check /LJlog/WiFi_Check
#./dropbox_uploader.sh upload /home/pi/upload.sh /LJlog/upload.sh
#./dropbox_uploader.sh upload /var/log/cron.log /LJlog/cron.log
#./dropbox_uploader.sh upload /home/xj1alarm.py /LJlog/xj1alarm.py
#./dropbox_uploader.sh upload /home/pi/crontab.txt /LJlog/crontab.txt
sudo rm /home/pi/wifilog.log
sudo rm /home/log.txt
sudo rm /home/pi/crontab.log

