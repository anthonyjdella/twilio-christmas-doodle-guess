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


def send_outbound_text(msg=None, media=None):
    try:
        message = client.messages.create(
            from_=os.getenv('MY_TWILIO_NUMBER'),
            to=os.getenv('ANTHONYS_NUMBER'),
            body=msg,
            media_url=media
        )
        print(message.body)
    except TwilioRestException as e:
        print(e)
        raise


# send_outbound_text('Trying to convince everyone to celebrate Christmas in the summer be like...', 'https://media.giphy.com/media/YPOgPxL7mED4IXoqLG/giphy.gif')


def quick_draw():
    try:
        qd = QuickDrawData()
        drawing = qd.get_drawing(random.choice(categories))
        drawing.animation.save('../images/quickdraw.gif')
        return drawing.name
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
    return new_version_sid


def create_build(asset_version_sid):
    build = client.serverless \
        .v1 \
        .services(service_sid) \
        .builds \
        .create(asset_versions=[asset_version_sid])
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


quick_draw()
host_asset()
print('https://pictionary-9376-dev.twil.io/images/quickdraw.gif')
# asset_version_sid = create_asset_version()
# build_sid = create_build(asset_version_sid)
# create_deployment(build_sid)
# create_deployment('ZBc9ee23df73696e087efb5cb1f5592f33')

# host_asset()



# 1st create a service, like a container
# service = client.serverless.v1.services.create(
#                                             include_credentials=True,
#                                             unique_name='pictionary',
#                                             friendly_name='pictionary-christmas'
#                                         )
# print(service.sid)


# 2nd create an environment, like dev, stage, prod
# environment = client.serverless \
#                     .v1 \
#                     .services(service_sid) \
#                     .environments \
#                     .create(domain_suffix='dev', unique_name='dev-environment')
# print(environment.sid)


# 3rd create an asset (just the name) - Function SID FHXXX
# asset = client.serverless \
#               .v1 \
#               .services(service_sid) \
#               .assets \
#               .create(friendly_name='image')

# print(asset.sid)
# ZHe2298af3ec5efaf9d820df3ad5cf5660


# 4th create an asset version
# asset_sid = os.getenv("TWILIO_ASSET_SID")

# service_url = f'https://serverless-upload.twilio.com/v1/Services/{service_sid}'
# upload_url = f'{service_url}/Assets/{asset_sid}/Versions'

# file_contents = open('../images/quickdraw.gif', 'rb')

# # Create a new Asset Version
# response = requests.post(
#     upload_url,
#     auth=(account_sid, auth_token),
#     files={
#         'Content': ('../images/quickdraw.gif', file_contents, 'image/gif')
#     },
#     data={
#         'Path': '/images/quickdraw.gif',
#         'Visibility': 'public',
#     },
# )

# new_version_sid = json.loads(response.text).get("sid")
# print(new_version_sid)
# ZN033f9123e96a29e3114dee623fda5bb3
# ZNbad161c0ab6b7b54baa546eb5ccfdee4


# 5th upload function - new version SID

# 6th create a build - build SID ZBXXXX
# build = client.serverless \
#               .v1 \
#               .services(service_sid) \
#               .builds \
#               .create(asset_versions=['ZNbad161c0ab6b7b54baa546eb5ccfdee4'])
# print(build.sid)
# ZBe39229b8b23bf5f5ab265258f5943505
# ZB9d5ce6961007968a774d77bf01f61146


# 7th create a deployment - url is now live!
# deployment = client.serverless \
#                    .v1 \
#                    .services(service_sid) \
#                    .environments(env_sid) \
#                    .deployments \
#                    .create(build_sid='ZB9d5ce6961007968a774d77bf01f61146')

# print(deployment.sid)
# ZDe50eaaa9944534ca0e745ca3cecb6126
# ZDe7df8327bd441ec2f5016b5b2071e34f


# FOR NEW ASSETS, NEED STEPS 4-7
# quick_draw()


# def create_asset():
#     asset = client.serverless \
#             .v1 \
#             .services(os.getenv('TWILIO_SERVICE_SID')) \
#             .assets \
#             .create(friendly_name='pictionary')
#     return(asset.sid)


# def upload_media():
#     service_sid = os.getenv('TWILIO_SERVICE_SID')
#     asset_sid = os.getenv('TWILIO_ASSET_SID')

#     service_url = f'https://serverless-upload.twilio.com/v1/Services/{service_sid}'
#     upload_url = f'{service_url}/Assets/{asset_sid}/Versions'

#     file_contents = open('../images/quickdraw.gif', 'rb')

#     response = requests.post(
#         upload_url,
#         auth=(account_sid, auth_token),
#         files={
#             'Content': ('../images/quickdraw.gif', file_contents, 'image/gif')
#         },
#         data={
#             'Path': '/images/quickdraw.gif',
#             'Visibility': 'public',
#         },
#     )

#     print(response.text)
#     new_version_sid = json.loads(response.text).get("sid")
#     print(new_version_sid)

#     build = client.serverless \
#             .v1 \
#             .services(os.getenv('TWILIO_SERVICE_SID')) \
#             .builds \
#             .create(
#                 asset_versions=[new_version_sid]
#             )

#     print(build.sid)

# build = client.serverless \
#         .v1 \
#         .services(os.getenv('TWILIO_SERVICE_SID')) \
#         .builds('ZBXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX') \
#         .fetch()

# print(build.status)

#     deployment = client.serverless \
#                 .v1 \
#                 .services(os.getenv('TWILIO_SERVICE_SID')) \
#                 .environments(os.getenv('TWILIO_ENV_SID')) \
#                 .deployments \
#                 .create()

#     print(deployment.sid)

# def build_status():
#     build = client.serverless \
#         .v1 \
#         .services('ZScfc0eb49dc3bc498dd99e274caa46472') \
#         .builds('ZBf96decf8f2476acbfdf7776241f47ecf') \
#         .fetch()

#     print(build.status)


# def deploy():
#     deployment = client.serverless \
#                    .v1 \
#                    .services(os.getenv('TWILIO_SERVICE_SID')) \
#                    .environments(os.getenv('TWILIO_ENV_SID')) \
#                    .deployments \
#                    .create()

#     print(deployment.sid)


# send_outbound_text('Trying to convince everyone to celebrate Christmas in the summer be like...', 'https://media.giphy.com/media/YPOgPxL7mED4IXoqLG/giphy.gif')
# send_outbound_text('Guess this picture', 'https://media.giphy.com/media/YPOgPxL7mED4IXoqLG/giphy.gif')


# quick_draw()
# upload_media()
# build_status()
# deploy()
# print(create_asset())
