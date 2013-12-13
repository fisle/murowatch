# -*- coding: utf-8 -*-
import smtplib
from bs4 import BeautifulSoup
import urllib2
import re
from email.mime.text import MIMEText

URL = 'http://murobbs.plaza.fi/kannettavat-tietokoneet/'
TO = 'you@localhost'
FROM = 'me@localhost'
FILE = '/path/to/file.txt' # Saves items there so does not send email on them afterwards
SEARCH = 'search me' # What to search

# Open URL and put it contents to BeautifulSoup
response = urllib2.urlopen(URL)
html = response.read()
soup = BeautifulSoup(html)

# Get all thread titles on first page
threads = soup.find_all('td', {'id': re.compile('td_threadtitle.*')})

# Open our FILE and read it's contents into list
f = open(FILE, 'r')
lines = f.readlines()
counter = 0
for line in lines:
  lines[counter] = line.replace('\n', '') # Replace every linebreak in list
  counter += 1
f = open(FILE, 'a')

# Loop through every thread
for thread in threads:
  # Get title and url
  title = thread.div.a.string.lower()
  url = thread.div.a.get('href')
  # Check if our SEARCH is found
  if title.find(SEARCH) is not -1:
    # Check title if it's sold already
    if title.find('myyty') is -1:
      # Check if we have emailed for it already
      if url not in lines:
        # Nope? Here's an email
        msg = MIMEText(url)
        msg['Subject'] = 'OH DOG'
        msg['From'] = FROM
        msg['To'] = TO
        s = smtplib.SMTP('localhost')
        s.sendmail(FROM, TO, msg.as_string())
        s.quit()
        # Write newline to our FILE
        f.write(url+'\n')

f.close()
