# import smtplib, ssl
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
#
#
# # set up the smtp server
# s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
# s.starttls()
# s.login('manutencaoluz@outlook.com', 'Aaa-11111')
#
# # create a message
# msg = MIMEMultipart()
#
# message = 'Corpo do email'
#
# # setup parameter of the message
# msg['From'] = 'manutencaoluz@outlook.com'
# msg['To'] = 'engleoluz@hotmail.com'
# msg['Subject'] = 'Teste de email'
#
# # add in the message body
#
# msg.attach(MIMEText(message, 'plain'))
#
# # send the message via the server
# s.send_message(msg)
#
# del msg






import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config


# # set up the smtp server
# s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
# s.starttls()
# s.login('manutencaoluz@outlook.com', 'Aaa-11111')
#
# # create a message
# msg = MIMEMultipart()
#
# message = 'Corpo do email'
#
# # setup parameter of the message
# msg['From'] = 'manutencaoluz@outlook.com'
# msg['To'] = 'engleoluz@hotmail.com'
# msg['Subject'] = 'Teste de email'
#
# # add in the message body
#
# msg.attach(MIMEText(message, 'plain'))
#
# # send the message via the server
# s.send_message(msg)
#
# del msg


# class Email(object):
#     _host = ""
#     _port = ""
#     _address = ""
#     _password = ""
#
#     def __init__(self, app=None):
#         if app is not None:
#             self.init_app(app)
#
#     def init_app(self, app):
#         self._host = app.config.get('MAIL_HOST')
#         self._port = app.config.get('MAIL_PORT')
#         self._address = app.config.get('MAIL_ADDRESS')
#         self._password = app.config.get('MAIL_PASSWORD')
#
#
#
#
#
# def create_module(app, **kwargs):
#
#
# class Email_man:
#     def __init__(self):
#         self.host = config.Config.MAIL_HOST
#         self.port = config.Config.MAIL_PORT
#         self.address = config.Config.MAIL_ADDRESS
#         self.password = config.Config.MAIL_PASSWORD
#
#     def send_mail(self, recipients, subject, message):
#         s = smtplib.SMTP(host=self.host, port=self.port)
#         s.starttls()
#         s.login(self.address, self.password)
#
#         # create a message
#         msg = MIMEMultipart()
#
#         # setup parameter of the message
#         msg['From'] = self.address
#         msg['To'] = recipients
#         msg['Subject'] = subject
#
#         # add in the message body
#         msg.attach(MIMEText(message, 'plain'))
#
#         # send the message via the server
#         s.send_message(msg)


#
# Email_man().send_mail(recipients='engleoluz@hotmail.com',
#                       subject='teste email POO 2',
#                       message='corpo da mensagem   2')
