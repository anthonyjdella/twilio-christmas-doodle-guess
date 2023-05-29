from quick_draw import send_outbound_text

import os
import random
import re
from flask import Flask, request, session
from flask_session import Session
from redis import Redis


app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = Redis(host='10.81.58.85', port='6379')

asset_urls = [
    "https://xmas-5474.twil.io/46-telephone.gif",
    "https://xmas-5474.twil.io/44-alarm%20clock.gif",
    "https://xmas-5474.twil.io/47-skateboard.gif",
    "https://xmas-5474.twil.io/48-airplane.gif",
    "https://xmas-5474.twil.io/45-laptop.gif",
    "https://xmas-5474.twil.io/49-train.gif",
    "https://xmas-5474.twil.io/50-bear.gif",
    "https://xmas-5474.twil.io/43-bear.gif",
    "https://xmas-5474.twil.io/34-tennis%20racquet.gif",
    "https://xmas-5474.twil.io/38-tennis%20racquet.gif",
    "https://xmas-5474.twil.io/35-oven.gif",
    "https://xmas-5474.twil.io/39-shoe.gif",
    "https://xmas-5474.twil.io/40-firetruck.gif",
    "https://xmas-5474.twil.io/41-bicycle.gif",
    "https://xmas-5474.twil.io/42-guitar.gif",
    "https://xmas-5474.twil.io/37-bear.gif",
    "https://xmas-5474.twil.io/36-skateboard.gif",
    "https://xmas-5474.twil.io/32-train.gif",
    "https://xmas-5474.twil.io/33-truck.gif",
    "https://xmas-5474.twil.io/28-laptop.gif",
    "https://xmas-5474.twil.io/24-drums.gif",
    "https://xmas-5474.twil.io/29-guitar.gif",
    "https://xmas-5474.twil.io/27-wristwatch.gif",
    "https://xmas-5474.twil.io/31-book.gif",
    "https://xmas-5474.twil.io/25-telephone.gif",
    "https://xmas-5474.twil.io/30-backpack.gif",
    "https://xmas-5474.twil.io/26-airplane.gif",
    "https://xmas-5474.twil.io/15-skateboard.gif",
    "https://xmas-5474.twil.io/21-shoe.gif",
    "https://xmas-5474.twil.io/18-bear.gif",
    "https://xmas-5474.twil.io/17-headphones.gif",
    "https://xmas-5474.twil.io/16-skateboard.gif",
    "https://xmas-5474.twil.io/19-airplane.gif",
    "https://xmas-5474.twil.io/20-train.gif",
    "https://xmas-5474.twil.io/23-truck.gif",
    "https://xmas-5474.twil.io/22-drums.gif",
    "https://xmas-5474.twil.io/11-helicopter.gif",
    "https://xmas-5474.twil.io/9-truck.gif",
    "https://xmas-5474.twil.io/10-train.gif",
    "https://xmas-5474.twil.io/8-bear.gif",
    "https://xmas-5474.twil.io/14-bicycle.gif",
    "https://xmas-5474.twil.io/12-oven.gif",
    "https://xmas-5474.twil.io/13-bear.gif",
    "https://xmas-5474.twil.io/3-firetruck.gif",
    "https://xmas-5474.twil.io/4-diamond.gif",
    "https://xmas-5474.twil.io/6-drums.gif",
    "https://xmas-5474.twil.io/5-bus.gif",
    "https://xmas-5474.twil.io/7-headphones.gif",
    "https://xmas-5474.twil.io/2-book.gif",
    "https://xmas-5474.twil.io/1-truck.gif"
]
drawing_name = None
is_playing = False

Session(app)


def initialize_game():
    session.clear()
    session['playing'] = False
    session['lives'] = 3


def start_new_game(user_number):
    initialize_game()
    session['playing'] = True
    random_url = random.choice(asset_urls)
    filename = os.path.basename(random_url)
    img_name = re.sub(r'\d+[-]', '', filename)
    img_name = re.sub(r'\.gif$', '', img_name)
    session['drawing_name'] = img_name
    send_outbound_text(user_number,
                       'Guess the Christmas gift Santa 🎅 is making!\n\nYou have 3 guesses remaining.',
                       random_url
                       )


def handle_bad_guess(user_number):
    session['lives'] -= 1
    if session['lives'] == 0:
        send_outbound_text(user_number,
                           f"Sorry, you ran out of attempts! Game over. 💔\n\nThe correct answer was: {session['drawing_name']}"
                           )
        initialize_game()
    else:
        send_outbound_text(user_number,
                           f"Try again ❌. You have {session['lives']} guesses remaining."
                           )


def handle_good_guess(user_number):
    send_outbound_text(user_number, 'Correct ✅! You guessed it!')
    initialize_game()


@app.route("/game", methods=['POST'])
def receive_inbound_text():
    user_input = request.values.get('Body', None).lower()
    user_number = request.values.get('From')

    if 'playing' not in session:
        initialize_game()

    if not session['playing']:
        if 'go' in user_input:
            start_new_game(user_number)
        else:
            send_outbound_text(user_number, 'To play a new game, send "GO"')
    else:
        if user_input in session['drawing_name']:
            handle_good_guess(user_number)
        else:
            handle_bad_guess(user_number)
    return '200'


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)
