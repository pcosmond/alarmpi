

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
global TemperaturePollInterval
global EmailDelay
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

input_value = GPIO.input(11)
input_value2 = GPIO.input(15)
input_value3 = GPIO.input(16)
input_value4 = GPIO.input(18)

user="simulatorrta@flighttrainingadelaide.com"    
password="simulator" 
smtp_server="smtp.gmail.com"  
smtp_user="simulatorsmtp@gmail.com"    
smtp_pass="simulator"    
sendto1="simulator@flighttrainingadelaide.com"
sendto2="pcosmond@bigpond.com"
over_temp= "The RTA Simulator Room is Over a Safe Temperature Limit"
power_failure= "The Power to the RTA simulator room has failed"
PrintToScreen=True
TempDiff=15
PrintToScreen=True
GPIOPollInterval=300
TemperaturePollInterval=300
EmailDelay=300
MaxTemp=28

def GetTemperature():
    
    global TempDiff
    global input_value
    global input_value2
    global input_value3
    global input_value4
    global elapsed_email_time
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
    filename = "/sys/bus/w1/devices/28-0000043e2b74/w1_slave"
    tfile = open(filename)
    text = tfile.read()
    tfile.close()
    filename2 = "/home/log.txt"
    tfile = open(filename2,'a')
    text2 = tfile.write('Time Stamp = ' + time.asctime() + '\n')
    text2 = tfile.write('Temp string = ' + text + '\n')
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
    filename4 = "/home/log.txt"
    tfile = open(filename4,'a')
    texti = tfile.write('Time Stamp = ' + time.asctime() + '\n')
    texti = tfile.write(temperaturedata + '   ' )
    tfile.close()
    if PrintToScreen: print temp
    if PrintToScreen: print input_value
    if PrintToScreen: print input_value2
    if PrintToScreen: print input_value3
    if PrintToScreen: print input_value4
    if PrintToScreen: print elapsed_email_time
    TempDiff= MaxTemp - temp
    if TempDiff<3: print "OverTemp"
    if TempDiff<3: SendEmailAlert(over_temp)
    if PrintToScreen: print TempDiff
    temp = round(temp,2)
    return(temp);
  
def SendEmailAlert(warning):
    import smtplib
    global PrintToScreen
    global elapsed_email_time
    global EmailDelay
    global start_email_time
    from email.mime.text import MIMEText
    RecordSet = True   
    if (elapsed_email_time > EmailDelay):
        start_email_time = time.time()    
        for i in range(1):
            addr_to   = sendto1
            addr_from = smtp_user      
            msg = MIMEText(warning)
            msg['To'] = addr_to 
            msg['From'] = addr_from
            msg['Subject'] = 'Alarm Notification' 
            s = smtplib.SMTP(smtp_server,587)
            s.ehlo()
            s.starttls()
            s.ehlo
            s.login(smtp_user,smtp_pass)
            s.sendmail(addr_from, addr_to, msg.as_string())
            s.quit()
            if PrintToScreen: print msg;

            addr_to   = sendto2
            addr_from = smtp_user    
            msg = MIMEText(warning)
            msg['To'] = addr_to 
            msg['From'] = addr_from
            msg['Subject'] = 'Alarm Notification' 
            s = smtplib.SMTP(smtp_server,587)
            s.ehlo()
            s.starttls()
            s.ehlo
            s.login(smtp_user,smtp_pass)
            s.sendmail(addr_from, addr_to, msg.as_string())
            s.quit()
            if PrintToScreen: print msg;
       

def PollRoutine():
    global start_time
    global elapsed_time
    global start_temperature_time
    global elapsed_temperature_time
    global GPIOPollInterval                 

    if (elapsed_time > GPIOPollInterval):
        start_time = time.time()
        NotifyHostTemperature()
        login1 =  GetDataFromHost(2,[0])
        if PrintToScreen: print login1

def NotifyHostTemperature():
    TempBuffer = []
    TempBuffer.append(GetTemperature())
    TempBuffer.append(0)
    rt=UpdateHost(14, TempBuffer)
    return (0)
    
def NotifyHostGPIO(GPIOnumber):
    rt=UpdateHost(13,[GPIOnumber])
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
        return False
    temp=rt.read()
    if PrintToScreen: print temp
    if temp=="TRUE":
        return(1)
    else:
        return(0)
      
def isNumber(x):
    try:
        val = int(x)
    except ValueError:
        return False
    return True

def find_all(a_str, sub):
    start = 0
    cnt=0
    while True:
        start = a_str.find(sub, start)
        if start == -1: 
            return cnt
        start += len(sub)
        cnt=cnt+1
        
def GetDataFromHost(function,opcode):
# Request data and receive reply (request/reply) from the server
 
    global user
    global password
    print "Sending request to server:"
    script_path = "http://www.privateeyepi.com/alarmhost.php?u="+user+"&p="+password+"&function="+str(function)
    i=0
    for x in opcode:
        script_path=script_path+"&opcode"+str(i)+"="+str(opcode[i])
        i=i+1
                
    print script_path 
    try:
        rt = urllib2.urlopen(script_path)
    except urllib2.HTTPError:
        return False
    print "Receiving reply from server:"
    temp=rt.read()
    print temp
    filename3 = "/home/log.txt"
    tfile = open(filename3,'a')
    text3 = tfile.write('Reply from server = '+ temp + '\n' + '\n')
    tfile.close()    
    l = find_all(temp,"/n");
    RecordSet = temp.split(',')
    c=[]
    y=0
    c.append([])
    for x in RecordSet:
        if x=="/n":
            y=y+1
            if y < l:
                c.append([])
        else:
            if isNumber(x):
                c[y].append(int(x))
            else:
                c[y].append(x)
        if find_all(x,"/FALSE")<>0:
            return False    
    return(c)

    
start_time = time.time()
start_temperature_time = time.time()
start_email_time = time.time()

while True:    
     
    elapsed_time = time.time() - start_time
    elapsed_temperature_time = time.time() - start_temperature_time
    elapsed_email_time = time.time() - start_email_time
    
    PollRoutine()   
    time.sleep(.2)

