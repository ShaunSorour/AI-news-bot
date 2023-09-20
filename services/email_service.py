from dotenv import load_dotenv
load_dotenv()
import os
import smtplib
from email.mime.text import MIMEText


sender = os.getenv("sender")
receiver = os.getenv("receiver")
smtp_server = os.getenv("smtp_server")
smtp_port = os.getenv("smtp_port")
smtp_pass = os.getenv("smtp_pass")


def send_email():
    sender_email = sender
    receiver_email = receiver

    html = open("news.html")
    msg = MIMEText(html.read(), "html")
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Breaking News"

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender, smtp_pass)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully.")
        server.quit()
    except Exception as e:
        print("Error sending email:", e)