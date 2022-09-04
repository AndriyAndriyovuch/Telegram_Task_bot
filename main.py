import json
import time

from reportlab import xrange
from telebot import TeleBot
from data.main_data import token


bot = TeleBot(token)
URL = 'https://api.telegram.org/bot' + token + '/'
COMMANDS = ['/start', '/add', '/current', '/long', '/all', '/delete']


@bot.message_handler(commands=['start'])
def send_message(message):
    bot.send_message(chat_id=message.chat.id, text=f'This is the list of commands: {COMMANDS}')


@bot.message_handler(commands=['add'])
def add_task(message):
    if message.text == '/add':
        bot.reply_to(message, text='Please write the task in format: \n '
                                   'name, deadline(01.01.2001), current/long \n'
                                   'For example: \n\n /add Make lunch, 01.12.2022, current')

    data = message.text.split(',')

    if len(data) != 3 and message.text != '/add':
        bot.reply_to(message, text='Wrong format, maybe try without comma')
    if len(data) == 3:
        task_type = data[-1].lower().replace(' ', '')

        if task_type == 'current':
            filename = 'data/current_tasks.json'
        elif task_type == 'long':
            filename = 'data/long_range_tasks.json'
        else:
            bot.reply_to(message, text='Wrong format (current/long')

        try:
            with open(filename, 'r') as file:
                data_json = json.load(file)

                if len(data_json) == 0:
                    task_id = 1
                else:
                    task_id = data_json[-1]['id'] + 1

                name = data[0]
                new_task = {'Name': name[5:],
                            'Deadline': data[1],
                            'id': task_id
                            }

                data_json.append(new_task)

                with open(filename, 'w') as file_2:
                    json.dump(data_json, file_2)
                bot.reply_to(message, text='Task created successfully')
        except Exception:
            pass


@bot.message_handler(commands=['current'])
def show_current_tasks(message):
    with open('data/current_tasks.json', 'r') as current_file:
        current_data = json.load(current_file)
        print(current_data)
        for data in current_data:
            result = f"Name: {data['Name']}\n" \
                     f"Deadline: {data['Deadline']}\n"\
                     f"id: {data['id']}\n"
            bot.send_message(message.chat.id, text=result)

@bot.message_handler(commands=['long'])
def show_long_tasks(message):
    with open('data/long_range_tasks.json', 'r') as long_file:
        long_data = json.load(long_file)
        print(long_data)
        for data in long_data:
            result = f"Name: {data['Name']}\n" \
                     f"Deadline: {data['Deadline']}\n" \
                     f"id: {data['id']}\n"
            bot.send_message(message.chat.id, text=result)


@bot.message_handler(commands=['delete'])
def delete_task(message):
    if message.text == '/delete':
        bot.reply_to(message, text='Please write the task in format: \n '
                                   'ID, current/long \n'
                                   'For example: \n\n /delete 13 current')

    data = message.text.split(' ')
    print('data=', data)
    if len(data) != 3 and message.text != '/delete':
        bot.reply_to(message, text='Wrong format')
    if len(data) == 3:
        task_type = data[-1].lower().replace(' ', '')

        if task_type == 'current':
            filename = 'data/current_tasks.json'
        elif task_type == 'long':
            filename = 'data/long_range_tasks.json'
        else:
            bot.reply_to(message, text='Wrong format (current/long')

        try:
            print('i tried')
            task_id = int(data[1])
            print('task_id =', task_id)
            with open(filename, 'r') as file:
                data_json = json.load(file)

                for i in xrange(len(data_json)):
                    if data_json[i]["id"] == task_id:
                        data_json.pop(i)

                        with open(filename, 'w') as file_2:
                            json.dump(data_json, file_2)
                        bot.reply_to(message, text='Task deleted successfully')
                        break
                    else:
                        bot.reply_to(message, text='Task not found')
        except Exception:
            pass


bot.infinity_polling()
