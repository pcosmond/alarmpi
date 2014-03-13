

import smtplib
from email.mime.text import MIMEText
from datetime import date 

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "simulatorsmtp@gmail.com"
SMTP_PASSWORD = "simulator"

EMAIL_FROM = "Test Email"
EMAIL_TO = ["posmond@clovermail.com", "pcosmond@bigpond.com"]
EMAIL_SPACE = ", "
EMAIL_SUBJECT = "Alarm Test : "
DATE_FORMAT = "%d/%m/%Y"

def SendEmailAlert(warning):         
    msg = MIMEText (warning)
    msg['To'] = EMAIL_SPACE.join(EMAIL_TO)
    msg['From'] = EMAIL_FROM
    msg['Subject'] = EMAIL_SUBJECT + " %s" % (date.today().strftime(DATE_FORMAT))
    s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    s.ehlo()
    s.starttls()
    s.ehlo
    s.login (SMTP_USER,SMTP_PASSWORD) 
    s.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    s.quit()

if __name__=='__main__':
    SendEmailAlert()
