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
        print("heeeeeeeeeeeeeeeeeeeee")
        server = smtplib.SMTP('smtp.mail.yahoo.com', 587)  # Replace with your SMTP server
        print('do we get here?')
        server.starttls()
        server.login(config.email_user, config.email_password)
        print('user: ', config.email_user, 'Passw: ', config.email_password)
        print('user: ', os.environ['EMAIL_USER'], 'Passw: ', os.environ['EMAIL_PASSWORD'])
        text = msg.as_string()
        print('message:', text)
        server.sendmail(config.email_user, config.email_to, text)
        server.quit()
        print('Email sent successfully')
    except Exception as e:
        print(f'Failed to send email: {e}')


if __name__ =="__main__":
    found_avx_items = search_avx_for_item(config.item_to_search)
    send_email(subject='Ethosz!!!', body=found_avx_items)