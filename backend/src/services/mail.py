from smtplib import SMTP
from email.message import EmailMessage
from ..core.config import SMTP_HOSTNAME, SMTP_PORT, DELABA_MAIL

def build_login_email(login, password):
    res = EmailMessage()
    res.set_content(f"Ваши данные для первоначального входа в Delaba\nЛогин: {login}\nПароль: {password}")
    res['Subject'] = 'Приглашение в Delaba'
    res['From'] = DELABA_MAIL
    res['To'] = login

    return res


def send_login_details(login, password):
    msg = build_login_email(login, password)

    with SMTP(SMTP_HOSTNAME, SMTP_PORT) as m:
        m.connect(SMTP_HOSTNAME, SMTP_PORT)
        m.send_message(msg)
