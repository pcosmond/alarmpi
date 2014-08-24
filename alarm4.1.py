# Generic 4.1 update for multiple temp sensors all sections

import time
import RPi.GPIO as GPIO
import urllib2
import subprocess  
#import Adafruit_CharLCD as LCD # use for LCD ***
import math
global user
global password
global EmailWarning
global smtp_server
global smtp_user
global smtp_pass
global GPIOPollInterval
global GetTemp
global MaxTemp
global sendto1
global sendto2
global over_temp
global EmailTimeDelay
global LoggingTimeDelay
global ElapsedEmailDelay   
global input_value
global input_value2
global input_value3
global input_value4
global GPIOnumber
global TempSensorGPIO
global TempSensorDirectory
TempSensorGPIO = []
TempSensorGPIO.append(7) #Sensor GPIO
TempSensorGPIO.append(88) #Sensor GPIO
TempSensorGPIO.append(89) #Sensor GPIO
TempSensorGPIO.append(90) #Sensor GPIO
TempSensorDirectory = []
TempSensorDirectory.append("28-0000043df3d8") #Change for sensor
TempSensorDirectory.append("28-000004d411d2") #Change for sensor
TempSensorDirectory.append("28-000004d50689") #Change for sensor
TempSensorDirectory.append("28-000004d496ee") #Change for sensor
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)
GPIO.setup(11, GPIO.IN)
GPIO.setup(15, GPIO.IN)
GPIO.setup(16, GPIO.IN)
GPIO.setup(18, GPIO.IN)
input_value = GPIO.input(11)
input_value2 = GPIO.input(15)
input_value3 = GPIO.input(16)
input_value4 = GPIO.input(18)  
# email settings
user='posmond@flighttrainingadelaide.com'                                      #change privateeyeuser to suit
password='simulator'                                             #change passwrd to suit
smtp_server="smtp.gmail.com"                                     #change smpt server to suit
smtp_port= 587                                                   #change port to suit
EMAIL_FROM= "peter "                                        #change from to suit
EMAIL_SPACE=", "
EMAIL_SUBJECT="Test Simulator Alarm"                                     #Change subject to suit
DATE_FORMAT= "%d/%m/%Y"  
smtp_user="simulatorsmtp@gmail.com"                              #change smtp user to suit
smtp_pass="simulator"                                            #change smtp passwd to suit
sendto1="simulator@flighttrainingadelaide.com"                                 #change send to to suit
sendto2="pcosmond@bigpond.com"                                   #change send to to suit  
#lcd = LCD.Adafruit_CharLCDPlate() #LCD entry
# Messages
over_temp= "The  room is over a safe Temperature limit"           #change msg to suit
power_failure= "The Power to the  has failed.  "                           #change messg to suit   
email_test= "Daily Email Test - Email operational for test Simulator "                                #change messg to suit  
# logfile name
filename = "/home/log.txt"                                       #Change messg to suit  
# numerical variables
TempDiff=15                                                      #log filename
GPIOPollInterval=30                                              #change GPIO polling interval to suit
MaxTemp=28                                #change max temp to suit, trip temp is this temp minus 3 degrees.
EmailTimeDelay=44000                                             # Delay until test email is sent
LoggingTimeDelay=300                                            #change Privateeyepi logging time delay to suit
ElapsedEmailDelay=300                                            #Delay until email is armed - resent

def GetTemperatureEmail():    #Email sending triggers
    global TempDiff
    global input_value
    global input_value2
    global input_value3
    global input_value4
    global elapsed_email_delay
    global elapsed_email_time
    global elapsed_host_delay
    global elapsed_time
    tfile = open(filename,'a')
    text1 = tfile.write('\n' + '----------------------------------' +  '\n' +  'Start of 30 second Temperature Log' + '\n')
    tfile.close()
    input_value = GPIO.input(11)
    if input_value == 3: 
        tfile = open(filename,'a')
        text1 = tfile.write('Power Failure 1' + '\n')
        tfile.close()
        SendEmailAlert(power_failure + "  Number 1 Supply")
#        lcd.set_color(1.0, 0.0, 0.0) #LCD Entry
#        lcd.clear()  #LCD Entry
#        lcd.message("Number 1 Supply" + "\n" + "  Failed") #LCD Entry
#        time.sleep(5.0) #LCD Entry
    input_value2 = GPIO.input(15)
    if input_value2 == 3: 
        tfile = open(filename,'a')
        text1 = tfile.write('Power Failure 2' + '\n')
        tfile.close()
        SendEmailAlert(power_failure + "  Number 2 Supply")
    input_value3 = GPIO.input(16)
    if input_value3 == 3: 
        tfile = open(filename,'a')
        text1 = tfile.write('Power Failure 3' + '\n')
        tfile.close()
        SendEmailAlert(power_failure + "  Number 3 Supply")
    input_value4 = GPIO.input(18)
    if input_value4 == 3: 
        tfile = open(filename,'a')
        text1 = tfile.write('Power Failure 4' + '\n')
        tfile.close()
        SendEmailAlert(power_failure + "  Number 4 Supply")   
    subprocess.call(['modprobe', 'w1-gpio'])
    subprocess.call(['modprobe', 'w1-therm'])
    filenamet = "/sys/bus/w1/devices/28-0000043df3d8/w1_slave"
    tfile = open(filenamet)
    text = tfile.read()
    tfile.close()
    tfile = open(filename,'a')
    text1 = tfile.write('Time Stamp =    ' + time.asctime() + '\n')
    text1 = tfile.write('Temp string = ' + text + '\n')
    eml = str(elapsed_email_delay)
    eml2 = str(elapsed_email_time)
    text1 = tfile.write('Email delay     ' + eml + '\n')
    text1 = tfile.write('Elapsed Email   ' + eml2 + '\n')
    tfile.close()
    print text
    firstline = text.split("\n")[0]
    crc = firstline.split(" ")[11]
    print "crc error = " + str(crc)
    if crc == "YES":
        secondline = text.split("\n")[1]
        temperaturedata = secondline.split(" ")[9]
        temperature = float(temperaturedata[2:])
        print temperature
        temperature = temperature / 1000
        tempe = float(temperature)
        tfile = open(filename,'a')
        text1 = tfile.write('Time Stamp = ' + time.asctime() + '\n')
        text1 = tfile.write('Temp monitor = ' + str(tempe) + 'Degrees' +  '\n')
        tfile.close()
        print 'Elapsed Email Test 44000   ' + str(elapsed_email_delay)
        print 'Email 300 sec delay        ' + str(elapsed_email_time)
        print '300  sec  Host Delay       ' + str(elapsed_host_delay) 
        print '30 second GPIO Delay       ' + str(elapsed_time)
        print 'Tempe   ' + str(tempe)
        print input_value
        print input_value2
        print input_value3
        print input_value4
        TempDiff= MaxTemp - tempe
        if TempDiff<3: print "OverTemp"
        if TempDiff<3: SendEmailAlert("Temperature is " + str(tempe) + "  Degrees")
        print str(TempDiff) + '\n' + '\n' + 'End of Temp Section Waiting ----' + '\n'
        temp = round(tempe,2)   
        tfile = open(filename,'a')
        text1 = tfile.write('End of Temp Monitor Section' + '\n')
        tfile.close()
#        if TempDiff>3: # LCD Entry
#            lcd.set_color(0.0, 1.0, 0.0) #LCD Entry
#            lcd.clear() #LCD Entry
#            message = "Temperature = " + "\n" +  str(tempe) + "  Degrees" #LCD Entry
#            lcd.message (message) #LCD Entry
#        if TempDiff<3: #LCD Entry
#            lcd.set_color(1.0, 0.0, 0.0) #LCD Entry
#            lcd.clear() #LCD Entry
#            message = "Temperature = " + "\n" + str(tempe) + "  Degrees" #LCD Entry
#            lcd.message (message) #LCD Entry
        return(temp)
    return (0)

def GetTemperature(no):        # (no) for Sensor number Privateeyepi triggers
    global TempDiff
    global input_value
    global input_value2
    global input_value3
    global input_value4
    global elapsed_email_delay
    tfile = open(filename,'a')
    text1 = tfile.write('\n' +  'Start of 5 minute Temperature Log' + '\n')
    tfile.close()
    input_value = GPIO.input(11)
    if input_value == 3: 
        NotifyHostGPIO(11)
    input_value2 = GPIO.input(15)
    if input_value2 == 3: 
        NotifyHostGPIO(15)
    input_value3 = GPIO.input(16)
    if input_value3 == 3: 
        NotifyHostGPIO(16)
    input_value4 = GPIO.input(18)
    if input_value4 == 3: 
        NotifyHostGPIO(18)
    subprocess.call(['modprobe', 'w1-gpio'])
    subprocess.call(['modprobe', 'w1-therm'])
    filenamer = "/sys/bus/w1/devices/" + TempSensorDirectory[no]+"/w1_slave"
    tfile = open(filenamer)
    text = tfile.read()
    tfile.close()
    print text
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    print temperaturedata
    temperature = float(temperaturedata[2:])
    print temperature
    temperature = temperature / 1000
    tempe = float(temperature)
    temp = round(tempe,2)
    return(temp)
  
def SendEmailAlert(warning):      #email section
    import smtplib
    global elapsed_email_time
    global EmailDelay
    global start_email_dly
    from email.mime.text import MIMEText
    from datetime import date
    if (elapsed_email_time > ElapsedEmailDelay):
        start_email_dly = time.time()
        addr_to = (sendto1, sendto2)
        addr_from = smtp_user      
        msg = MIMEText(warning)
        msg['To'] = EMAIL_SPACE.join(addr_to)
        msg['From'] = EMAIL_FROM
        msg['Subject'] = EMAIL_SUBJECT + " %s" %(date.today().strftime(DATE_FORMAT))
        try:
           s = smtplib.SMTP(smtp_server, smtp_port)
           s.ehlo()
           s.starttls()
           s.ehlo
           s.login(smtp_user,smtp_pass)
        except smtplib.SMTPException:
            return (0)
        else:
            try:
               s.sendmail(addr_from, addr_to, msg.as_string())
               s.quit()
               print msg;
               print "email sent ok"
               tfile = open(filename,'a')
               text1 = tfile.write(str(msg) + '\n')
               text1 = tfile.write('Email sent ok' + '\n')
               tfile.close()
            except (smtplib.SMTPDataError, smtplib.SMTPRecipientsRefused, smtplib.SMTPSenderRefused):
               print "SMTP_Error"
               tfile = open(filename,'a')
               text1 = tfile.write('SMTP Error' + '\n')
               tfile.close()
               return (0)
            except (smtplib.SMTPAuthenticationError, smtplib.SMTPException, smtplib.SMTPServerDisconnected ):
               print "SMTPError 2"
               tfile = open(filename,'a')
               text1 = tfile.write('SMTP2 Error' + '\n')
               tfile.close()
               return (0)
    return (0)


def NotifyHostTemperature(gpio):      # Multiple sensor Section to send temp data to Privateeyepi via UpdateHost()
    tfile = open(filename,'a')
    text1 = tfile.write('NotifyHostTemp_Start')
    tfile.close()
    TempBuffer = []
    TempBuffer.append(GetTemperature(gpio))#Multiple sensor
    TempBuffer.append(0)
    TempBuffer.append(TempSensorGPIO[gpio])#Multiple Sensor
    rt=UpdateHost(14, TempBuffer)  
    print "Notify Host Temperature"
    tfile = open(filename,'a')
    text1 = tfile.write('Temp Buffer Host  ' + str(TempBuffer) + '\n')
    text1 = tfile.write('End of Notify Host Temp Section' + '\n')
    tfile.close()
    return (rt)
  
  
def NotifyHostGPIO(GPIOnumber):        # Section to send Power Alerts to Privateeyepi via UpdateHost()
    tfile = open(filename,'a')
    text1 = tfile.write('NotifyHostGPIO_Start')
    tfile.close()
    rt=UpdateHost(13,[GPIOnumber]) 
    tfile = open(filename,'a')
    text1 = tfile.write('Notify Host GPIO Number  ' + str(GPIOnumber) + '\n')
    text1 = tfile.write('End of NotifyHostGPIO Section' + '\n')
    tfile.close()
    return(rt)


def UpdateHost(function,opcode):        # Section to send data to Privateeyepi
    global user
    global password
    script_path = "https://privateeyepi.com/alarmhostr.php?u="+user+"&p="+password+"&function="+str(function)
    i=0
    for x in opcode:
        script_path=script_path+"&opcode"+str(i)+"="+str(opcode[i])
        i=i+1
    print "Host Update: "+ script_path
    tfile = open(filename,'a')
    text1 = tfile.write("Host Update" + script_path  + '\n')
    tfile.close() 
    try:
        rt=urllib2.urlopen(script_path)
        tfile = open(filename,'a')
        text1 = tfile.write('Update Host successful' + '\n')
        tfile.close()
        print "Host Update Satisfactory"
        report = rt.read()
    except urllib2.HTTPError:
        print "HTTP Error text"
        tfile = open(filename,'a')
        text = tfile.write('HTTP Error text' + '\n')
        tfile.close()
        return (0)
    except urllib2.URLError:
        print "URL Error text" 
        tfile = open(filename,'a')
        text1 = tfile.write('URL Error' + '\n')
        tfile.close()
        return (0)
    print report + "   Rt read"
#    lcd.set_color(0.0, 0.0, 1.0) #LCD Entry
#    lcd.clear() #LCD Entry
#    lcd.message("Host Update " + "\n" + "Satisfactory") #LCD Entry
#    time.sleep(10.0) #LCD Entry
    tfile = open(filename,'a')
    text1 = tfile.write('End of Update Host' + '\n')
    tfile.close()
    print "End of Update Host"
    return(0)

def PollRoutine():         # Timing poll section
    global start_time
    global elapsed_time
    global start_email_delay
    global elapsed_email_delay
    global GPIOPollInterval 
    global EmailTimeDelay                
    global start_host_delay
    if (elapsed_time > GPIOPollInterval):
        start_time = time.time()
        print 'Start GPIO Interval' + '\n'
        GetTemperatureEmail() 
    if (elapsed_email_delay > EmailTimeDelay):
        start_email_delay = time.time()
        print 'Start Email test' + '\n'
        SendEmailAlert(email_test)
    if (elapsed_host_delay > LoggingTimeDelay):
        start_host_delay = time.time()
        print 'Start Host Upload' + '\n'
        NotifyHostTemperature(0) #Sensor Number
        NotifyHostTemperature(1) #Sensor Number
        NotifyHostTemperature(2) #Sensor Number
        NotifyHostTemperature(3) #Sensor Number
    return (0)
    
# Main 

start_time = time.time()
start_email_delay = time.time()
start_host_delay = time.time()
start_email_dly = time.time()

while True:    
    elapsed_time = time.time() - start_time
    elapsed_email_delay = time.time() - start_email_delay
    elapsed_host_delay = time.time() - start_host_delay
    elapsed_email_time = time.time() - start_email_dly

    PollRoutine()   
    time.sleep(.2)



