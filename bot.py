import os

from flask import Flask, request

import telebot

from timetable import TimeTable

TOKEN = '1083066191:AAGXKSutCPElXS_jRbtmjZnShXbNItPps0k'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

#chat_id = bot.get_updates()[-1].message.chat_id

@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)
    text = "I can help you to remember timetable in univercity\
        or name of your techer\n\n\
            You can control me by sending these commands:\n\n\
                You can control me by sending these commands:\n\n\
                    /timetable-show timetable in form and \
                        period of time what you like\n\
                            /name-show full name of teacher which\
                                you choice"
    bot.reply_to(message, text)
    #bot.send_message(chat_id=chat_id, text=text)
    
@bot.message_handler(commands=['timetable'])
def simple_timetable(message):
    t = TimeTable("old_timetable.json")
    text = t.print_days("week")
    bot.reply_to(message, text)
    #bot.send_message(chat_id=chat_id, text=text)

"""
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)
"""

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://stormy-falls-05476.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
