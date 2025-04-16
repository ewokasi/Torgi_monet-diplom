import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import asyncio


async def send_mail(recipient: str, theme: str, body: str):
    smtp_server = "smtp.beget.com"
    smtp_port = 465  # or 587 for TLS
    username = "test@monety.shop"
    password = "!Nn25111978"

    sender = "test@monety.shop"
    subject = theme

    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        async with aiosmtplib.SMTP(hostname=smtp_server, port=smtp_port, use_tls=True) as server:
            await server.login(username, password)
            await server.send_message(message)
            print("Письмо отправлено успешно!")
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")


if __name__ =="__main__":
    asyncio.run(send_mail("kostyakov0203@mail.ru", "123", "123"))
