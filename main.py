import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config
import os

found_items = []

def search_avx_for_item(item_to_search):
    try:
        for url in config.urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.find_all('a', class_='topictitle')
            searched_item = item_to_search
            
            for item in items:
                if searched_item.lower() in item.text.lower():
                    print(f'Item found: {item.text}')
                    found_items.append(item.text.strip())
        found_items_multiline = '\n'.join(found_items)
        return found_items_multiline
    except requests.HTTPError as err:
        if err.response.status_code != 200:
            error_message = f'Something went wrong..{err.response.status_code}'
            return error_message


def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = config.email_user
    msg['To'] = config.email_to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:     
        print("Starting SSL connection to SMTP server...")
        server = smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465)  # Connect using SSL
        server.login(config.email_user, config.email_password)
        # server.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASSWORD'])
        print('Logged in as:', config.email_user)
        text = msg.as_string()
        print('Message content:', text)
        server.sendmail(config.email_user, config.email_to, text)
        # server.sendmail(os.environ['EMAIL_USER'], os.environ['EMAIL_TO'], text)
        server.quit()
        print('Email sent successfully')
    except Exception as e:
        print(f'Failed to send email: {e}')


if __name__ =="__main__":
    found_avx_items = search_avx_for_item(config.item_to_search)
    send_email(subject='Ethosz!!!', body=found_avx_items)