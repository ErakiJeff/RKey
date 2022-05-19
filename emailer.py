import yagmail
import os

auth_file = os.path.join(os.path.dirname(__file__), 'oauth2_creds.json')

def send_email(item, recipeient):
    yag = yagmail.SMTP(oauth2_file=auth_file)
    subject = f"You have just recieved {item}!"
    
    yag.send(recipeient, subject=subject)