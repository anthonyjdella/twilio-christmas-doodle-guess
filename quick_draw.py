import os
import requests
import json
import random
import polling

from dotenv import load_dotenv
from quickdraw import QuickDrawData
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
service_sid = os.getenv("TWILIO_SERVICE_SID")
env_sid = os.getenv("TWILIO_ENV_SID")
asset_sid = os.getenv("TWILIO_ASSET_SID")
asset_version_sid = None
build_sid = None

client = Client(account_sid, auth_token)

categories = [
    "airplane",
    "alarm clock",
    "backpack",
    "bear",
    "bicycle",
    "binoculars",
    "book",
    "bus",
    "camera",
    "computer",
    "diamond",
    "drums",
    "firetruck",
    "guitar",
    "headphones",
    "helicopter",
    "laptop",
    "oven",
    "shoe",
    "skateboard",
    "telephone",
    "tennis racquet",
    "train",
    "truck",
    "wristwatch"
]


def send_outbound_text(to=None, body=None, media_URL=None):
    try:
        message = client.messages.create(
            from_=os.getenv('MY_TWILIO_NUMBER'),
            to=to,
            body=body,
            media_url=media_URL
        )
        print(message.body)
    except TwilioRestException as e:
        print(e)
        raise


def quick_draw():
    try:
        qd = QuickDrawData()
        drawing = qd.get_drawing(random.choice(categories))
        drawing.animation.save('../images/quickdraw.gif')
        return drawing.name
    except Exception as e:
        print(e)


def quick_draw_50_images():
    try:
        qd = QuickDrawData()
        counter = 0
        drawing_names = []
        for i in range(1,51):
            drawing = qd.get_drawing(random.choice(categories))
            drawing.animation.save(f"../images/{i}-{drawing.name}.gif")
            drawing_names.append(drawing.name)
            counter += 0
    except Exception as e:
        print(e)


def host_asset():
    asset_version_sid = create_asset_version()
    build_sid = create_build(asset_version_sid)
    create_deployment(build_sid)


def create_asset_version():
    service_url = f'https://serverless-upload.twilio.com/v1/Services/{service_sid}'
    upload_url = f'{service_url}/Assets/{asset_sid}/Versions'

    file_contents = open('../images/quickdraw.gif', 'rb')

    response = requests.post(
        upload_url,
        auth=(account_sid, auth_token),
        files={
            'Content': ('../images/quickdraw.gif', file_contents, 'image/gif')
        },
        data={
            'Path': '/images/quickdraw.gif',
            'Visibility': 'public',
        },
    )

    new_version_sid = json.loads(response.text).get("sid")
    print(new_version_sid)
    return new_version_sid


def create_build(asset_version_sid):
    build = client.serverless \
        .v1 \
        .services(service_sid) \
        .builds \
        .create(asset_versions=[asset_version_sid])
    print(build.sid)
    return build.sid


def check_build_status(build_sid):
    build = client.serverless \
        .v1 \
        .services(service_sid) \
        .builds(build_sid) \
        .fetch()
    print(build.status)
    return build.status


def is_completed(response):
    return response == 'completed'


def create_deployment(build_sid):
    polling.poll(
        lambda: check_build_status(build_sid),
        check_success=is_completed,
        step=5,
        timeout=30
    )

    deployment = client.serverless \
        .v1 \
        .services(service_sid) \
        .environments(env_sid) \
        .deployments \
        .create(build_sid=build_sid)
    print(deployment.sid)


# Steps
# 1st create a service, like a container
# 2nd create an environment, like dev, stage, prod
# 3rd create an asset (just the name) - Function SID FHXXX
# 4th create an asset version
# 5th upload function - new version SID
# 6th create a build - build SID ZBXXXX
# 7th create a deployment - url is now live!
