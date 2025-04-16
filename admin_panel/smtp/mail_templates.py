import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from routers.clientsCRUD.get_mails import get_mails_to_notify, get_mails_to_notify_start
from routers.clientsCRUD.get_by_phone import get_by_phone
from routers.clientsCRUD.embeded_get_client import get as c_get
from .mail_parts import parts
from deco import try_decorator
from globals import smtp_username, smtp_password


async def send_mail(recipient: str, theme: str, body: str):
    smtp_server = "smtp.beget.com"
    smtp_port = 465  # or 587 for TLS
    username = smtp_username
    password = smtp_password

    sender = smtp_username  
    subject = theme

    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    print("Отправка на", recipient)
    try:
        async with aiosmtplib.SMTP(hostname=smtp_server, port=smtp_port, use_tls=True) as server:
            await server.login(username, password)
            await server.send_message(message)
            print("Письмо отправлено успешно!", theme)
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")


@try_decorator
async def mass_auction_started(Name: str, url: str):
    target = await get_mails_to_notify_start()
    print("mass_auction_started")
    print(target)
    for person in target:
        await send_mail(person['email'], parts["header_auction_start"] + Name, parts["body_default"]+ url)
        print(person)


@try_decorator
async def mass_news(Name: str, body: str):
    target = await get_mails_to_notify()
    for person in target:
        await send_mail(person['mail'], Name, body)


@try_decorator
async def target_bet_beated(c_id: str):
    target = await c_get(c_id)
    print("target", target)
    if target["mail_receive_bet_beated"] == True:
        await send_mail(target["email"], parts['header_bet_beated'], parts["body_default"])


from routers.auctionCRUD.get_highest_bet import get_highest_bet


@try_decorator
async def target_won_auction(a_id):
    # Await the coroutine before accessing its result
    highest_bet = await get_highest_bet(a_id)  # Await the coroutine
    clients_id = highest_bet["clients_id"]  # Now you can access clients_id safely

    target = await c_get(clients_id)  # Assuming c_get is also an async function
    if target["get_mails"] == 1:
        await send_mail(target["email"], parts['header_you_won'], parts["body_you_won"])


# If you need to run an example, wrap it in an async context or use an event loop
# Example:
# import asyncio
# asyncio.run(target_won_auction("some_id"))
