from threading import Thread
from flask import current_app, render_template

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import config


def send_email(subject, recicipients, html):
    message = Mail(
        from_email=config.Config.MAIL_FROM,
        to_emails=recicipients,
        subject=subject,
        html_content=html)
    try:
        sg = SendGridAPIClient(config.Config.SENDGRID_API_KEY)
        response = sg.send(message)
    except Exception as e:
        print(e.message)

# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)
#
#
# def send_email(to, subject, template, **kwargs):
#     app = current_app._get_current_object()
#     msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
#                   sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
#     msg.body = render_template(template + '.txt', **kwargs)
#     msg.html = render_template(template + '.html', **kwargs)
#     thr = Thread(target=send_async_email, args=[app, msg])
#     thr.start()
#     return
