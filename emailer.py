import yagmail
import os
from config_reader import get_data

email_sender = get_data("email_sender")
email_recipient = get_data("email_recipient")

auth_file = os.path.join(os.path.dirname(__file__), "data/oauth2_creds.json")

yag = yagmail.SMTP(email_sender, oauth2_file=auth_file)


def send_email(item, recipeient=email_recipient):
    subject = f"You have just recieved {item}!"
    yag.send(recipeient, subject=subject)
