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
    MAIL_TLS=config("MAIL_TLS"),
    MAIL_SSL=config("MAIL_SSL"),
    USE_CREDENTIALS=config("USE_CREDENTIALS"),
    TEMPLATE_FOLDER='app/email'
)

async def send_email(subject: str, recipient: List, context: str):
   message = MessageSchema(
        subject=subject,
        recipients= recipient,
        body=context,
        subtype="html"
    )
   fm = FastMail(email_send)
   await fm.send_message(message)
