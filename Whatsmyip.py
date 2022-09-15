#!/usr/bin/python3

# Wrote by: Ryan Gillette
# Date:     2018-09-17
# Updated:  2019-12-16
# Purpose:  Check for external IP change, if changed, update route53 and send email
# Cron Example "*/5 * * * * python3 /path/to/Whatsmyip.py mailgun_password AWS_profile"

import smtplib, os, sys, argparse, urllib.request, sqlite3, logging, logging.handlers
import modules.vars as vars
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from aws_utils import aws_route53, aws_route53_record_value

# 3rd Party modules
import boto3

# save users home directory as path
path = os.path.join(os.environ["HOME"])
credentials_file = os.path.join(path, "credentials")

# Set up a specific logger with our desired output level
LOG_FILENAME = os.path.join(path, 'Whatsmyip.log')
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.INFO)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=200000, backupCount=3)

# logger Formatting
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt='%m/%d/%Y %I:%M:%S %p'
    )
handler.setFormatter(formatter)

my_logger.addHandler(handler)

# SMTP Password passed in when ran 
mailgun_password = str(sys.argv[1])

# AWS Profile to use 2nd var
profile = str(sys.argv[2])

# AWS Route53 Connection
session = boto3.Session(profile_name=profile)
client = session.client('route53')

# Test Internet connection and get current IP
def internet_up():
    try:
        my_logger.info("Testing Internet Connection")
        urllib.request.urlopen('https://ident.me', timeout=1)
        return True
    except urllib.error.HTTPError as err:
        my_logger.error(err)
        return False

# sends email set vars in modules/vars.py 
def sendmail(ip):
    fromaddr = vars.mailgun_from
    toaddr = [vars.mailgun_email, vars.mailgun_second_email]
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = ','.join(toaddr)
    msg['Subject'] = 'External IP Changed'

    body = 'Your new IP is ' + ip + ". Entries in Route53 have been updated!"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.mailgun.org', 587)
        server.starttls()
        server.login(vars.mailgun_login, mailgun_password)
        server.sendmail(fromaddr, toaddr, msg.as_string())
        server.quit()
    except Exception as err:
        my_logger.error(err)

def main():
    # Testing internet connection
    if internet_up():
        currentIP = urllib.request.urlopen('https://ident.me').read().decode('utf8')
        my_logger.info("Internet is up")
        
        # Compare old external IP to current IP
        ip = aws_route53_record_value(vars.domain, client, vars.hostedZoneId, 'A')
    
        if ip != currentIP:
            my_logger.info('Adding or updating ' + vars.domain + ' to Route53')
            aws_route53(
                vars.domain, 
                'UPSERT', ' is being created or updated', 
                currentIP, client, vars.hostedZoneId, "A"
                )

            my_logger.info("Sending Email with new IP")
            sendmail(ip)

        else:
            my_logger.info("IP did not change")

    else:
        my_logger.info("No Internet")

if __name__ == "__main__":
    main()
