from flask import Flask, request
import telebot
import os
from ratelimit import limits, sleep_and_retry


TOKEN = os.getenv("api_key")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
URL = "https://echobot-d3d3.onrender.com/"


# Set the rate limit to 1 message per second
@sleep_and_retry
@limits(calls=1, period=1)
def send_message(chat_id, text):
    bot.send_message(chat_id=chat_id, text=text)

@bot.message_handler(commands=["start", "help"])
def handle_commands(message):
    send_message(message.chat.id, "Let's play a game!")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    send_message(message.chat.id, message.text)

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=URL + TOKEN)
    return "!", 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))