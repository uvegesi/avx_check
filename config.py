import os

urls = ['https://avxforum.hu/forum/viewforum.php?f=64',
            'https://avxforum.hu/forum/viewforum.php?f=64&sid=70d662223359609be8192b6e76c25195&start=25',
            'https://avxforum.hu/forum/viewforum.php?f=64&&start=50'
            ]

email_user = os.environ["EMAIL_FROM"]
email_password = os.environ["SOME_SECRET"]
email_to = os.environ["EMAIL_TO"]

item_to_search = 'Ethosz'
