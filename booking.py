"""
- A library room booking crawler (with email confirmation) from my university years 
- Books a room for two hours on person 1 and next two hours on person 2.
- credentials.json and token.pickle files to be obtained from https://developers.google.com/people/quickstart/python
"""

from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pickle
import os.path
import selenium
import datetime
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def notify(title, sub_message):
    print(title + " " + sub_message)


room = "108"
hour1 = "19:00"  # Specify first 4 hours of booking.
hour2 = "20:00"
hour3 = "21:00"
hour4 = "22:00"
hour5 = "23:00"  # Only for 24 the time is 23:59 else it is 00:00,01:00 etc

gecko_path = r"/home/PycharmProjects/geckodriver"
library_url = 'library.com/booking/teamstudy' # template library urls
library_confirmation_url = "library.com/confirmation"
login_name1 = "name1"
login_surname1 = "surname1"
login_email1 = "username1@gmail.com"
login_name2 = "name2"
login_surname2 = "surname2"
login_email2 = "username2@gmail.com"
currentDT = datetime.datetime.today() + datetime.timedelta(days=2)
print(currentDT)
options = Options()
options.headless = True
browser = webdriver.Firefox(options=options, executable_path=gecko_path)
browser.get()

try:
    if (1 == currentDT.day) or (2 == currentDT.day):
        browser.find_element_by_class_name("ui-datepicker-next.ui-corner-all").click()

    browser.find_element_by_link_text(str(currentDT.day)).click()
    browser.find_element_by_xpath(
        '//*[@title="' + room + ', ' + hour1 + ' to ' + hour2 + ', ' +
        str(currentDT.day) + '/' + str(currentDT.month) + '/' + str(currentDT.year) + '"]').click()
    time.sleep(2)
    browser.find_element_by_xpath(
        '//*[@title="' + room + ', ' + hour2 + ' to ' + hour3 + ', ' +
        str(currentDT.day) + '/' + str(currentDT.month) + '/' + str(currentDT.year) + '"]').click()
    browser.find_element_by_name('Continue').click()
    browser.find_element_by_id('fname').send_keys(login_name1)
    browser.find_element_by_id('lname').send_keys(login_surname1)
    browser.find_element_by_id('email').send_keys(login_email1)
    browser.find_element_by_id('s-lc-rm-sub').click()
    notify("Booking", "Library room " + room + " is booked between: " + hour1 + " - " + hour3)
except (selenium.common.exceptions.NoSuchElementException, Exception) as e:
    notify("Booking", "Library room: " + room + " could not be reserved between " + hour1 + " - " + hour3)

browser.refresh()
time.sleep(5)
browser.refresh()
time.sleep(5)

try:
    if (1 == currentDT.day) or (2 == currentDT.day):
        browser.find_element_by_class_name("ui-datepicker-next.ui-corner-all").click()

    browser.find_element_by_link_text(str(currentDT.day)).click()
    browser.find_element_by_xpath(
        '//*[@title="' + room + ', ' + hour3 + ' to ' + hour4 + ', ' +
        str(currentDT.day) + '/' + str(currentDT.month) + '/' + str(currentDT.year) + '"]').click()
    time.sleep(2)
    browser.find_element_by_xpath(
        '//*[@title="' + room + ', ' + hour4 + ' to ' + hour5 + ', ' +
        str(currentDT.day) + '/' + str(currentDT.month) + '/' + str(currentDT.year) + '"]').click()
    browser.find_element_by_name('Continue').click()
    browser.find_element_by_id('fname').send_keys(login_name2)
    browser.find_element_by_id('lname').send_keys(login_surname2)
    browser.find_element_by_id('email').send_keys(login_email2)
    browser.find_element_by_id('s-lc-rm-sub').click()
    notify("Booking", "Library room " + room + " is booked between " + hour3 + " - " + hour5)
except (selenium.common.exceptions.NoSuchElementException, Exception) as e:
    notify("Booking", "Library room " + room + " could not be reserved between " + hour3 + " - " + hour5)


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
time.sleep(40)

creds = None
if os.path.exists('token1.pickle'):
    with open('token1.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials1.json', SCOPES)
        creds = flow.run_local_server()
    with open('token1.pickle', 'wb') as token:
        pickle.dump(creds, token)
service = build('gmail', 'v1', credentials=creds)
results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
messages = results.get('messages', [])
inbox = []
link = None

if not messages:
    notify("Booking", "First inbox is empty.")
else:
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        inbox.append(msg['snippet'])
inbox.reverse()

for my_str in inbox:
    line = my_str.split()
    for k in line:
        if library_confirmation_url in k:
            linem = k.split("&")
            link = linem[0] + "&" + linem[1][4:]

if link is None:
    notify("Booking", "First booking mail could not be found.")
else:
    try:
        browser.get(link)
        browser.find_element_by_id('rm_confirm_link').click()
        notify("Booking", "First booking mail is confirmed.")
    except (selenium.common.exceptions.NoSuchElementException, Exception)as e:
        notify("Booking", "First booking mail could not be confirmed.")

creds2 = None
if os.path.exists('token2.pickle'):
    with open('token2.pickle', 'rb') as token2:
        creds2 = pickle.load(token2)
if not creds2 or not creds2.valid:
    if creds2 and creds2.expired and creds2.refresh_token:
        creds2.refresh(Request())
    else:
        flow2 = InstalledAppFlow.from_client_secrets_file('credentials2.json', SCOPES)
        creds2 = flow2.run_local_server()
        # Save the credentials for the next run
    with open('token2.pickle', 'wb') as token2:
        pickle.dump(creds2, token2)
service2 = build('gmail', 'v1', credentials=creds2)
results2 = service2.users().messages().list(userId='me', labelIds=['INBOX']).execute()
messages2 = results2.get('messages', [])
inbox2 = []
link2 = None

if not messages2:
    notify("Booking", "Second inbox is empty.")
else:
    for message2 in messages2:
        msg2 = service2.users().messages().get(userId='me', id=message2['id']).execute()
        inbox2.append(msg2['snippet'])
inbox2.reverse()

for my_str2 in inbox2:
    line2 = my_str2.split()
    for k2 in line2:
        if library_confirmation_url in k2:
            line3 = k2.split("&")
            link2 = line3[0] + "&" + line3[1][4:]


if link2 is None:
    notify("Booking", "Second booking mail could not be found.")
else:
    try:
        browser.get(link2)
        browser.find_element_by_id('rm_confirm_link').click()
        notify("Booking", "Second booking mail is confirmed.")
    except (selenium.common.exceptions.NoSuchElementException, Exception) as e:
        notify("Booking", "Second booking email could not be confirmed.")


browser.close()
