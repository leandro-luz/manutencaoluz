import logging
from threading import Thread

from flask import current_app, render_template
from flask_mail import Message

from webapp import mail
from webapp.sistema.models import LogsEventos
from .decorator import async_

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)


@async_
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs) -> bool:
    try:
        app = current_app._get_current_object()
        msg = Message(subject)
        msg.sender = app.config['MAIL_SENDER']
        msg.recipients = [to]
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        Thread(name='enviar_email', target=send_async_email, args=(app, msg)).start()
        send_async_email(app, msg)
        return True
    except Exception as e:
        LogsEventos.registrar("erro", send_email.__name__, erro=e)
        return False
