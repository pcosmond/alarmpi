cd /home/pi/Dropbox-Uploader
./dropbox_uploader.sh upload /home/pi/wifilog.log /fftxlog/wifilog.log 
./dropbox_uploader.sh upload /home/log.txt /fftxlog/log.txt
./dropbox_uploader.sh upload /home/pi/crontab.log /fftxlog/crontab.log
#./dropbox_uploader.sh upload /home/pi/emailtst.py /fftxlog/emailtst.py
#./dropbox_uploader.sh upload /home/pi/WiFi_Check /fftxlog/WiFi_Check
#./dropbox_uploader.sh upload /home/pi/upload.sh /fftxlog/upload.sh
#./dropbox_uploader.sh upload /var/log/cron.log /fftxlog/cron.log
#./dropbox_uploader.sh upload /home/fftxalarm.py /fftxlog/fftxalarm.py
#./dropbox_uploader.sh upload /home/pi/crontab.txt /fftxlog/crontab.txt
sudo rm /home/pi/wifilog.log
sudo rm /home/log.txt
sudo rm /home/pi/crontab.log

