from flask import Flask, request
import telebot
import os


api = os.getenv("api_key")
port = int(os.getenv("PORT", 5000))

app = Flask(__name__)
bot = telebot.TeleBot(token=api, threaded = False)
URL = "https://echobot-d3d3.onrender.com"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


# Webhook
@app.route('/' + api, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=URL + api)
    return "!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)