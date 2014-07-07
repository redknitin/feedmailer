#
# -=[ Y-News ]=-
# (Gotcha: This app is hard-coded to use GMail's SMTP)
# Description: Sends the Title and Link from the RSS Feed by email
# Instructions: Make updates to settings.ini and execute
# Dependencies: Requires BeautifulSoup4
#

__author__ = 'Nitin Reddy Katkam'

from urllib import request
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import configparser

cfg = configparser.ConfigParser()
cfg.read('settings.ini')


def get_data(url):
    """
    Fetches the data from the specified URL
    :param url:
    :return:
    """
    fh = request.urlopen(url)
    data = fh.read()
    fh.close()
    return data


def soupify_news():
    """
    Gets the soup object
    :return:
    """
    global cfg
    data = get_data(cfg['Feed']['URL'])
    soup = BeautifulSoup(data)
    return soup


def get_titleslinks():
    """
    Gets a string with the titles and links of the RSS feed
    :return:
    """
    items = soupify_news().findAll('item')
    #for iter in items:
    #    print(iter.title.string + '\n' + iter.link.string + '\n')
    return ''.join([(iter.title.string + '\n' + iter.link.string + '\n\n') for iter in items])


def send_email():
    """
    Main method
    :return:
    """
    global cfg
    from_email = cfg['Mail']['FromEmail']
    from_pass = cfg['Mail']['FromPass']
    to_email = cfg['Mail']['ToEmail']
    subject = cfg['Mail']['Subject']

    srv = smtplib.SMTP('smtp.gmail.com', 587)
    srv.ehlo()
    srv.starttls()
    srv.ehlo()
    srv.login(from_email, from_pass)

    msg = MIMEText(get_titleslinks())
    msg['Subject'] = subject
    srv.sendmail(from_email, to_email, msg.as_string())

    srv.quit()
    srv.close()

if __name__ == '__main__':
    send_email()
    print('Msg sent')
