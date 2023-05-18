from quick_draw import send_outbound_text
from quick_draw import quick_draw
from quick_draw import host_asset

from flask import Flask, request, session
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)
app.secret_key = 'super_secret_key'

asset_url = 'https://pictionary-9376-dev.twil.io/images/quickdraw.gif'
drawing_name = None
twiml = MessagingResponse()

is_playing = False


with app.app_context():
    drawing_name = quick_draw()
    host_asset()


@app.route("/pictionary", methods=['POST'])
def receive_inbound_text():
    session['drawing_name'] = drawing_name
    user_input = request.values.get('Body', None).lower()


    def handle_new_game():
        session['playing'] = True
        session['lives'] = 3
        print(session['playing'])
        send_outbound_text('Guess the Christmas gift Santa 🎅 is making!\n\nYou have 3 guesses remaining.', asset_url)


    def handle_invalid_game():
        send_outbound_text(f'To play a new game, send "GO"')


    def check_answer(user_input):
        if user_input in drawing_name:
            return True
        return False


    def handle_bad_guess():
        session['lives'] -= 1
        if session['lives'] == 0:
            handle_game_over()
            send_outbound_text(f"Sorry, you ran out of attempts! Game over. 💔\n\nThe correct answer was: {drawing_name}")
        else:
            send_outbound_text(f"Try again ❌. You have {session['lives']} guesses remaining.")


    def handle_good_guess():
        handle_game_over()
        send_outbound_text('Correct ✅! You guessed it!')


    def handle_game_over():
        session.clear()
        # drawing_name = quick_draw()
        # host_asset()


    if not session.get('playing'):
        print('inside')
        if 'go' in user_input:
            handle_new_game()
        else:
            handle_invalid_game()
    else:
        correct = check_answer(user_input)
        if not correct:
            handle_bad_guess()
        else:
            handle_good_guess()


    return '200'


app.run(host='localhost', debug=False, port=3000)
