# Main imports for server.
import os
from flask import Flask, request
import telebot
# My imports 
from timetable import TimeTable
from command_handler import text_messege, is_timetable_command, is_day, is_shape
from data_base_handler import add_user, give_timetable, give_week, is_ex_user, load_week, give_group, update_user_group

TOKEN = os.environ['TOKEN']
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

@bot.message_handler(commands=['start', 'help'])
def start(message):
    chat_id = message.chat.id
    text = text_messege('start')
    bot.send_message(chat_id, text)

@bot.message_handler(commands=['help_timetable'])
def help_timetable(message):
    chat_id = message.chat.id
    text = text_messege('help_timetable')
    bot.send_message(chat_id, text)
    
@bot.message_handler(commands=['timetable'])
def timetable(message):
    chat_id = message.chat.id
    if not is_ex_user(chat_id):
        text = "Probably you are new user, or bot was reload. Try to use \
 /group [your group] command"
        bot.send_message(chat_id, text=text)
        return None
    data = give_timetable(chat_id)
    week = give_week()
    t = TimeTable(data, week)
    command = message.text.split()
    shape = "brief"
    day = "today"
    week = "current"
    if is_timetable_command(command, t):
        for sub_command in command:
            if is_day(sub_command, t):
                day = sub_command
            if is_shape(sub_command):
                shape = sub_command
        if day == "week":
            text = t.print_week(shape, week)
        else:
            text = t.print_day(t.give_day(day), shape, week)
            if text:
                text = day + '\n' + text
            else:
                text = "В этот день нет пар"
    else:
        text = "Command error"
    bot.send_message(chat_id=chat_id, text=text)

@bot.message_handler(commands=['week'])
def week(message):
    chat_id = message.chat.id
    week = give_week() 
    bot.send_message(chat_id, text=week)

@bot.message_handler(commands=['group'])
def group_(message):
    chat_id = message.chat.id
    name = message.from_user.first_name
    if not is_ex_user(chat_id):
        try:
            group = message.text.split()[1]
            text = add_user(chat_id, name, group)
        except:
            text = "Command error"
    else:
        text = "User already exist"
    
    bot.send_message(chat_id, text=text)

@bot.message_handler(commands=['make_test'])
def make_tests(message):
    chat_id = message.chat.id
    name = message.from_user.first_name 
    if not is_ex_user(chat_id):
        try:
            group = message.text.split()[1]
            text = "Chat_id = {}, name = '{}', group = '{}'"
            text = text.format(str(chat_id), name, group)
        except:
            text = "Command error"
    else:
        text = "User already exist"
    bot.send_message(chat_id, text=text)
    

@bot.message_handler(commands=['update'])
def update(message):
    chat_id = message.chat.id
    new_group = message.text.split()[1]
    if not is_ex_user(chat_id):
        text = "Probably you are new user, or bot was reload. Try to use \
 /group [your group] command"
        bot.send_message(chat_id, text=text)
        return None
    text = update_user_group(chat_id, new_group)
    bot.send_message(chat_id, text=text)

@bot.message_handler(commands=['newweek'])
def newweek(message):
    chat_id = message.chat.id
    if not is_ex_user(chat_id):
        text = "Probably you are new user, or bot was reload. Try to use \
 /group [your group] command"
        bot.send_message(chat_id, text=text)
        return None
    group = give_group(chat_id)
    try:
        load_week(group)
        week = give_week()
        text = week
    except:
        text = "Somethink goes wrong"
    bot.send_message(chat_id, text=text)

# From this place start server part, don't touch.
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
