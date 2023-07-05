
# from dotenv import dotenv_values

import os

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python


from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# message = Mail(
#     from_email='engleoluz@hotmail.com',
#     to_emails='guguleo2019@gmail.com',
#     subject='Sending with Twilio SendGrid is Fun',
#     html_content='<strong>and easy to do anywhere, even with Python</strong>')
# try:
#     sg = SendGridAPIClient('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')
#     response = sg.send(message)
#     print(response.status_code)
#     print(response.body)
#     print(response.headers)
# except Exception as e:
#     print(e)


# print(environ.get('SENDGRID_API_KEY'))
for a in os.environ:
    print(a)

# config = dotenv_values("sendgrid.env", encoding="utf-8")
# print(config)