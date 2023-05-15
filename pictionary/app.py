from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)


@app.route("/pictionary", methods=['POST'])
def handle_incoming_sms():
    user_input = request.values.get('Body', None)
    transactions = get_transactions(user_input)

    resp = MessagingResponse()
    resp.message(transactions)

    return str(resp)


app.run(host='localhost', debug=True, port=8080)