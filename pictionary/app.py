from quick_draw import send_outbound_text
from quick_draw import quick_draw
from quick_draw import host_asset

from flask import Flask, request, session
from flask_session import Session
from flask_cors import CORS, cross_origin
from time import sleep
import threading


app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'

asset_url = 'https://pictionary-9376-dev.twil.io/images/quickdraw.gif'
drawing_name = None

is_playing = False

Session(app)


def initialize_game():
    session.clear()
    session['playing'] = False
    session['lives'] = 3


def start_new_game():
    initialize_game()
    session['playing'] = True
    session['drawing_name'] = quick_draw()

    countdown_thread = threading.Thread(target=send_countdown)
    countdown_thread.start()

    host_asset_thread = threading.Thread(target=host_asset_with_callback)
    host_asset_thread.start()


def send_asset_callback():
    send_outbound_text(
        'Guess the Christmas gift Santa 🎅 is making!\n\nYou have 3 guesses remaining.',
        asset_url
    )


def host_asset_with_callback():
    host_asset()
    sleep(5)
    send_asset_callback()


def send_countdown():
    send_outbound_text('Game is starting soon...')
    sleep(2)

    for i in range(5, 0, -1):
        send_outbound_text(str(i))
        sleep(2.5)


def handle_bad_guess():
    session['lives'] -= 1
    if session['lives'] == 0:
        send_outbound_text(
            f"Sorry, you ran out of attempts! Game over. 💔\n\nThe correct answer was: {session['drawing_name']}"
        )
        initialize_game()
    else:
        send_outbound_text(
            f"Try again ❌. You have {session['lives']} guesses remaining."
        )


def handle_good_guess():
    send_outbound_text('Correct ✅! You guessed it!')
    initialize_game()


@app.route("/pictionary", methods=['POST'])
def receive_inbound_text():
    user_input = request.values.get('Body', None).lower()

    if 'playing' not in session:
        initialize_game()

    if not session['playing']:
        if 'go' in user_input:
            start_new_game()
        else:
            send_outbound_text('To play a new game, send "GO"')
    else:
        if user_input == session['drawing_name']:
            handle_good_guess()
        else:
            handle_bad_guess()
    return '200'


app.run(host='localhost', debug=False, port=3000)
