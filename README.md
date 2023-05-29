# Twilio Christmas Doodle Guess


**MERRY CHRISTMAS** -- Did you know that was the first text message sent in 1992?

🎅 This is a Christmas-themed Doodle Guessing game built with Twilio SMS/MMS.

This game was presented during [Signal 2023](https://signal.twilio.com/) and [Twilio Startup Labs Denver](https://tsldenver.splashthat.com/).

It is deployed with Google App Engine and uses Memorystore to persist session data with Redis.


## How to play

Send a text message to `+1 (844) 905-5079`.

If you text `GO`, a new game will start.
You'll receive a message that asks you to guess the drawing of the animated .gif

You get 3 chances to guess.

![Playing the game](/gifs/usage.gif)


## Versions

There are 2 versions of the app (version 2 is preferred & what I am demoing)

1. Retrieve a random animated image and host it in real-time. This gives the user more variety in games they can play, however it takes a longer to host the images.
2. Images are already hosted and randomly selected from 50 pre-downloaded images. This is much faster, but images and games are repeated.

## How to run version 1

1. cd to `game`
2. Run `python3 app_threading.py` to deploy on `localhost:3000`
2. In a separate terminal, run `ngrok http 3000`
    - Or in my case `ngrok http --region=us --hostname=ngrok.[domain-name].com 3000`
3. Send a text to `+1 (844) 905-5079`


## How to run version 2

1. Run `python3 main.py` to deploy on `localhost:3000`
2. In a separate terminal, run `ngrok http 3000`
    - Or in my case `ngrok http --region=us --hostname=ngrok.[domain-name].com 3000`
3. Send a text to `+1 (844) 905-5079`


## Contact
If you'd like to learn more, reach out to me [@anthonyjdella](https://twitter.com/anthonyjdella).