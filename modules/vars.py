#!/usr/bin/python3

# Logfile name
logf = "Whatsmyip.log"

# domain Information
domain = 'example.com'
domains = [
  'test1.example.com',
  'test2.example.com'
    ]

# hosted zone ID
hostedZoneId = '<Replace with hostedZoneID from AWS Route53>'

# Mailgun config
mailgun_from = "from address for mailgun"
mailgun_email = "Email to send to"
mailgun_second_email = "Email to send to"
mailgun_login = "mailgun SMTP username"

# DB Name
dbname = 'whatsmyip.sqlite3'
