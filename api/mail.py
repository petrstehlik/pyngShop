#/bin/env python3

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import *

def sendmail(to, content):
	msg = MIMEMultipart()
	msg['From'] = CONFIG["email"]["username"]
	msg['To'] = to
	msg['Subject'] = "Order from pyngshop!"

	body = content

	msg.attach(MIMEText(body, 'plain'))

	server = smtplib.SMTP_SSL(CONFIG["email"]["server"], 465)

	server.login(CONFIG["email"]["username"], CONFIG["email"]["password"])

	text = msg.as_string()

	server.sendmail(CONFIG["email"]["username"], to, text)
	server.quit()


# sendmail("ahoj@petrstehlik.cz", "hello bitch")