import datetime as dt
import pandas as pd
import random
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")

if not MY_EMAIL or not MY_PASSWORD:
    print("Error: Email or Password not found in environment variables")
    exit(1)

now = dt.datetime.now()
today = now.day
this_month = now.month

data = pd.read_csv("birthdays.csv")

for (index, row) in data.iterrows():
    if row['day'] == today and row['month'] == this_month:
        name = row['name']
        gmail = row['email']
        n = random.randint(1, 3)
        with open(file=f"./letter_templates/letter_{n}.txt") as letter:
            letter_data = letter.read()
            letter_data = letter_data.replace("[NAME]", name)
            print(f"DEBUG: Sending birthday message to {name} ({gmail})")

        with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=gmail,
                                msg=f"Subject:Happy Birthday!!\n\n{letter_data}")

