import subprocess
import smtplib
import socket
from email.mime.text import MIMEText
import datetime
#Change to your own account information
to = ''#your email address
gmail_user = ''#your email address
gmail_password = ''#your email password
smtpserver = smtplib.SMTP('smtp.gmail.com',587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo
smtpserver.login(gmail_user, gmail_password)
today = datetime.date.today()
arg='ip route list'
p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
data = p.communicate()
split_data = data[0].split()
ipaddr = split_data[split_data.index('src')+1]
my_ip = 'Your ip is %s' % ipaddr
msg = MIMEText(my_ip)
msg['Subject']= 'IP For YURI on %s' %today.strftime('%b %d %Y')#YURI: myraspberrypi name
msg['From'] = gmail_user
msg['To'] = to
smtpserver.sendmail(gmail_user,[to],msg.as_string())
smtpserver.quit()
