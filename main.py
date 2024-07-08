import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

found_items = []
urls = ['https://avxforum.hu/forum/viewforum.php?f=64',
            'https://avxforum.hu/forum/viewforum.php?f=64&sid=70d662223359609be8192b6e76c25195&start=25',
            'https://avxforum.hu/forum/viewforum.php?f=64&&start=50'
            ]

email_user = os.environ["EMAIL_FROM"]
email_password = os.environ["SOME_SECRET"]
email_to = os.environ["EMAIL_TO"]

def search_avx_for_item(item_to_search):
    try:
        for url in urls:
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
    msg['From'] = email_user
    msg['To'] = email_to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.mail.yahoo.com', 587)  # Replace with your SMTP server
        server.starttls()
        server.login(email_user, email_password)
        text = msg.as_string()
        server.sendmail(email_user, email_to, text)
        server.quit()
        print('Email sent successfully')
    except Exception as e:
        print(f'Failed to send email: {e}')


if __name__ =="__main__":
    item = 'Ethosz'
    found_avx_items = search_avx_for_item(item)
    send_email(subject='Ethosz!!!', body=found_avx_items)