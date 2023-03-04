from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from webapp import mail
import logging

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    try:
        app = current_app._get_current_object()
        msg = Message(subject)
        msg.sender = app.config['MAIL_SENDER']
        msg.recipients = [to]
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        thr = Thread(target=send_async_email, args=[app, msg])
        thr.start()
        return thr
    except Exception as e:
        log.error(f'Erro ao tentar enviar email {to} : {e}')
