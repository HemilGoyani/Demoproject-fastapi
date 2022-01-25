from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import List
from starlette.config import Config

# load .env
config = Config(".env")
email_send = ConnectionConfig(
    MAIL_USERNAME=config('MAIL_USERNAME'),
    MAIL_PASSWORD=config("MAIL_PASSWORD"),
    MAIL_FROM=config("MAIL_FROM"),
    MAIL_PORT=config("MAIL_PORT"),
    MAIL_SERVER=config("MAIL_SERVER"),
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
)


def send_email(subject: str, recipient: List, message: str):
    message = MessageSchema(
        subject=subject,
        recipients= recipient,
        body=message,
        subtype="html"
    )
    fm = FastMail(email_send)
    fm.send_message(message)
