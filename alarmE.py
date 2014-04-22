# latest as from 22th April 2014 change for host error and 24 hour email test email section 

import time
import RPi.GPIO as GPIO
import urllib2
import subprocess
global user
global password
global AlarmActioned
global PrintToScreen 
global smtp_server
global smtp_user
global smtp_pass
global GPIOPollInterval
global GetTemp
global MaxTemp
global sendto1
global sendto2
global over_temp

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)
GPIO.setup(11, GPIO.IN)
GPIO.setup(15, GPIO.IN)
GPIO.setup(16, GPIO.IN)
GPIO.setup(18, GPIO.IN)

global input_value
global input_value2
global input_value3
global input_value4
global GPIOnumber
global elapsed_email_delay
input_value = GPIO.input(11)
input_value2 = GPIO.input(15)
input_value3 = GPIO.input(16)
input_value4 = GPIO.input(18)

user="pcosmond@bigpond.com"     #change privateeyeuser to suit
password="Peter2059"            #change passwrd to suit
smtp_server="smtp.gmail.com"    #change smpt server to suit
smtp_port= 587                  #change port to suit
EMAIL_FROM= "Peters Test"       #change from to suit
EMAIL_SPACE=", "
EMAIL_SUBJECT="peters test"      #Change subject to suit
DATE_FORMAT= "%d/%m/%Y"  
smtp_user="simulatorsmtp@gmail.com"    #change smtp user to suit
smtp_pass="simulator"                  #change smtp passwd to suit
sendto1="simulator@flighttrainingadelaide.com"         #change send to to suit
sendto2="pcosmond@bigpond.com"                         #change send to to suit
over_temp= "peters test **  Room is over a safe Temperature limit"     #change messg to suit
power_failure= "The Power test  Simulator has failed"       #change messg to suit   
email_test= "Daily Email Test - Email Operational for FFTX"  #change messg to suit
filename = "/home/log.txt"
PrintToScreen=True
TempDiff=15
PrintToScreen=True
GPIOPollInterval=300                                #change GPIO to suit
MaxTemp=35                  #change max temp to suit, trip temp is this temp minus 3 degrees.
EmailTimeDelay=300			# 86400

def GetTemperature():    
    global TempDiff
    global input_value
    global input_value2
    global input_value3
    global input_value4
    global elapsed_email_delay
    input_value = GPIO.input(11)
    if input_value == 1: NotifyHostGPIO(11)
    if input_value == 1: SendEmailAlert(power_failure)
    input_value2 = GPIO.input(15)
    if input_value2 == 1: NotifyHostGPIO(15)
    if input_value2 == 1: SendEmailAlert(power_failure)
    input_value3 = GPIO.input(16)
    if input_value3 == 1: NotifyHostGPIO(16)
    if input_value3 == 1: SendEmailAlert(power_failure)
    input_value4 = GPIO.input(18)
    if input_value4 == 1: NotifyHostGPIO(18)
    if input_value4 == 1: SendEmailAlert(power_failure)
    subprocess.call(['modprobe', 'w1-gpio'])
    subprocess.call(['modprobe', 'w1-therm'])
    filenamet = "/sys/bus/w1/devices/28-0000043df3d8/w1_slave"
    tfile = open(filenamet)
    text = tfile.read()
    tfile.close()
    tfile = open(filename,'a')
    text2 = tfile.write('\n' +  'Start of Log' + '\n')
    text2 = tfile.write('Time Stamp = ' + time.asctime() + '\n')
    text2 = tfile.write('Temp string = ' + text + '\n')
    eml = str(elapsed_email_delay)
    text2 = tfile.write('Email delay' + eml + '\n')
    tfile.close()
    print text
    secondline = text.split("\n")[1]
    print secondline 
    temperaturedata = secondline.split(" ")[9]
    print temperaturedata
    temperature = float(temperaturedata[2:])
    print temperature
    temperature = temperature / 1000
    temp = float(temperature)
    tfile = open(filename,'a')
    texti = tfile.write('Time Stamp = ' + time.asctime() + '\n')
    texti = tfile.write(temperaturedata + '\n' )
    texti = tfile.write('Temp mon section' + '\n')
    tfile.close()
    print elapsed_email_delay
    if PrintToScreen: print temp
    if PrintToScreen: print input_value
    if PrintToScreen: print input_value2
    if PrintToScreen: print input_value3
    if PrintToScreen: print input_value4
    TempDiff= MaxTemp - temp
    if TempDiff<3: print "OverTemp"
    if TempDiff<3: SendEmailAlert(over_temp)
    if PrintToScreen: print TempDiff
    temp = round(temp,2)   
    tfile = open(filename,'a')
    textf = tfile.write('End of Temp Section' + '\n')
    tfile.close()
    return(temp);
  
def SendEmailAlert(warning):
    import smtplib
    global PrintToScreen
    global elapsed_email_time
    global EmailDelay
    global start_email_time
    from email.mime.text import MIMEText
    from datetime import date
    RecordSet = True   
    addr_to   = [“simulator@fighttrainingadelaide.com”, pcosmond@bigpond.com ]
    addr_from = smtp_user      
    msg = MIMEText(warning)
    msg['To'] = addr_to 
    msg['From'] = EMAIL_FROM
    msg['Subject'] = EMAIL_SUBJECT + " %s" %(date.today().strftime(DATE_FORMAT))
    s = smtplib.SMTP(smtp_server, smtp_port)
    s.ehlo()
    s.starttls()
    s.ehlo
    try:
        s.login(smtp_user,smtp_pass)
        s.sendmail(addr_from, addr_to, msg.as_string())
        s.quit()
	    if PrintToScreen: print msg;
    except (smtplib.SMTPDataError, smtplib.SMTPrecipientsRefused, smtplib.SenderRefused):
        if PrintToScreen: print “SMTP_Error”
        tfile = open(filename,'a')
        texto = tfile.write('SMTP Error' + '\n')
        return (0)
    except (smtplib.SMTPAuthenticationError, smtplib.SMTPException, smtplib.SMTPServerDisconnected ):
        if PrintToScreen: print “SMTPError 2”
        tfile = open(filename,'a')
        textp = tfile.write('SMTP2 Error' + '\n')
        return (0)
    return (0)


def PollRoutine():
    global start_time
    global elapsed_time
    global start_email_delay
    global elapsed_email_delay
    global GPIOPollInterval 
    global EmailTimeDelay                
#    print elapsed_email_delay 
    if (elapsed_time > GPIOPollInterval):
        start_time = time.time()
        NotifyHostTemperature() 

    if (elapsed_email_delay > EmailTimeDelay):
	start_email_delay = time.time() 
	SendEmailAlert(email_test)
    return (0)

def NotifyHostTemperature():
    TempBuffer = []
    TempBuffer.append(GetTemperature())
    TempBuffer.append(0)
    rt=UpdateHost(14, TempBuffer)  
#    filename7 = "/home/log.txt"
    tfile = open(filename,'a')
    texth = tfile.write('End of Notify Host Temp Section' + '\n')
    return (0)
    
def NotifyHostGPIO(GPIOnumber):
    rt=UpdateHost(13,[GPIOnumber]) 
#    filename8 = "/home/log.txt"
    tfile = open(filename,'a')
    textj = tfile.write('End of Temp Section' + '\n')
    return(rt)

def UpdateHost(function,opcode):
    global user
    global password
    global PrintToScreen
    script_path = "https://privateeyepi.com/alarmhost.php?u="+user+"&p="+password+"&function="+str(function)
    i=0
    for x in opcode:
        script_path=script_path+"&opcode"+str(i)+"="+str(opcode[i])
        i=i+1
    if PrintToScreen: print "Host Update: "+script_path 
    try:
        rt=urllib2.urlopen(script_path)
    except urllib2.HTTPError:
        if PrintToScreen: print "HTTP Error"
#        filename9 = "/home/log.txt"
        tfile = open(filename,'a')
        textk = tfile.write('HTTP Error' + '\n')
        return (0)
    except urllib2.URLError:
        if PrintToScreen: print "URL Error" 
#        filenamea = "/home/log.txt"
        tfile = open(filename,'a')
        textl = tfile.write('End of Temp Section' + '\n')
        return (0)
#    temp=rt.read()
#    if PrintToScreen: print "Next print is temp rt.read"
#    if PrintToScreen: print temp
#    if temp=="TRUE":
#        return(1)
#    else:
#    filenameb = "/home/log.txt"
    tfile = open(filename,'a')
    textm = tfile.write('End of Update Host' + '\n')
    return(0)
    
start_time = time.time()
start_email_delay = time.time()

while True:    
     
    elapsed_time = time.time() - start_time
    elapsed_email_delay = time.time() - start_email_delay
    PollRoutine()   
    time.sleep(.2)


