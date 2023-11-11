import logging

from flask import current_app, render_template
from flask_mail import Message

from webapp import mail
from webapp.sistema.models import LogsEventos

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)


def send_email(to, subject, template, **kwargs) -> bool:
    try:
        app = current_app
        msg = Message(subject)
        msg.sender = app.config['MAIL_SENDER']
        msg.recipients = [to]
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        mail.send(msg)
        return True
    except Exception as e:
        LogsEventos.registrar("erro", send_email.__name__, erro=str(e))
        return False
