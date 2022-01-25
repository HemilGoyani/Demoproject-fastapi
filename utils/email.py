from fastapi_mail import FastMail, MessageSchema,ConnectionConfig

conf = ConnectionConfig(
   MAIL_USERNAME="goyanihemil8@gmail.com",
   MAIL_PASSWORD="hemil@123456789",
   MAIL_PORT=587,
   MAIL_SERVER="smtp.gmail.com",
   MAIL_TLS=True,
   MAIL_SSL=False
)