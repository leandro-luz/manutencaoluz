
# from dotenv import dotenv_values
import datetime
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
# for a in os.environ:
#     print(a)

# config = dotenv_values("sendgrid.env", encoding="utf-8")
# print(config)



def data_futura(tempo, unidade):
    """ Função que calcula e retorna uma data no futuro"""
    # Fator basico
    fator = 1
    # Verifica qual a unidade de tempo
    if unidade == "Mensal" or  \
            unidade == "Bimensal" or  \
            unidade == "Trimensal" or  \
            unidade == "Semestral":
        fator = 30
    if unidade == "Anual":
        fator  = 365

    # retorna a data futura
    return datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + \
           datetime.timedelta(days=tempo * fator)

print(data_futura(7, "Semanal"))
print(data_futura(1, "Mensal"))
print(data_futura(2, "Bimensal"))
print(data_futura(3, "Trimensal"))
print(data_futura(6, "Semestral"))
print(data_futura(1, "Anual"))
