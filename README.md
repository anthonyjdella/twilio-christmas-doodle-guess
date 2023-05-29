# Twilio Christmas Doodle Guess


**MERRY CHRISTMAS** -- Did you know that was the first text message sent in 1992?

🎅 This is a Christmas-themed Doodle Guessing game built with Twilio SMS/MMS.

This game was presented during [Signal 2023](https://signal.twilio.com/) and [Twilio Startup Labs Denver](https://tsldenver.splashthat.com/).


## How to play

Send a text message to `+1 (844) 905-5079`.

If you text `GO`, a new game will start.
You'll receive a message that asks you to guess the drawing of the animated .gif

You get 3 chances to guess.

![Playing the game](/gifs/usage.gif)

## How to run

1. Run `python3 app.py` to deploy on `localhost:3000`
2. In a separate terminal, run `ngrok http 3000`
    - Or in my case `ngrok http --region=us --hostname=ngrok.[domain-name].com 3000`
3. Send a text to `+1 (844) 905-5079`


## Contact
If you'd like to learn more, reach out to me [@anthonyjdella](https://twitter.com/anthonyjdella).