import json
from telebot import TeleBot
import requests

from data.main_data import token

bot = TeleBot(token)
URL = 'https://api.telegram.org/bot' + token + '/'
COMMANDS = ['/start', '/add_task', '/current_tasks', '/long_range_tasks', '/all_tasks', '/delete_task']

@bot.message_handler(commands=['start'])
def send_message(message):
    bot.send_message(chat_id=message.chat.id, text=f'This is the list of commands: {COMMANDS}')

@bot.message_handler(commands=['add_task'])
def send_message(message):
    bot.reply_to(message, text='Please write the task in format = "name, deadline( in_format 01.01.2001), current/long')
    data = message.text.split(',')

    task_type = data[-1].lower().replace(' ', '')


    if task_type == 'current':
        with open('data/current_tasks.json', 'r') as file:
            data_json = json.load(file)
            print(data_json)
            if len(data_json) == 0:
                task_id = 1
            else:
                task_id = data_json[-1]['id'] + 1

            name = data[0]
            new_task = {'name': name[10:],
                        'date': data[1],
                        'id': task_id
                        }

            data_json.append(new_task)

            with open('data/current_tasks.json', 'w') as file_2:
                json.dump(data_json, file_2)

bot.infinity_polling()