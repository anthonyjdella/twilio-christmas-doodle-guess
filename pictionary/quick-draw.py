import os

from dotenv import load_dotenv
from quickdraw import QuickDrawData
from twilio.rest import Client


load_dotenv()

qd = QuickDrawData()
anvil = qd.get_drawing("anvil")

print(anvil)

anvil.image.save("../images/my_anvil.gif")


def send_text(msg):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body = msg,
        from_ = os.getenv('MY_TWILIO_NUMBER'),
        to = os.getenv('ANTHONYS_NUMBER')
    )
    print(message.body)


send_text("ahoy, world")