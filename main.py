import json
import datetime
import time

from telebot import TeleBot, types
from data.main_data import token

bot = TeleBot(token)
URL = 'https://api.telegram.org/bot' + token + '/'
COMMANDS = ['/start', '/add', '/current', '/long', '/all', '/delete']


@bot.message_handler(commands=['start'])
def send_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    add = types.KeyboardButton('/add')
    current = types.KeyboardButton('/current')
    long = types.KeyboardButton('/long')
    all = types.KeyboardButton('/all')
    delete = types.KeyboardButton('/delete')
    markup.add(add, current, long, all, delete)
    bot.send_message(chat_id=message.chat.id, text=f'This is the list of commands: \n'
                                                   f'/add - Add a task\n'
                                                   f'/current - List of current tasks\n'
                                                   f'/long - List of long range tasks\n'
                                                   f'/all - List of all tasks\n'
                                                   f'/delete - Delete task', reply_markup=markup)

    filenames = ['data/current_tasks.json', 'data/long_range_tasks.json']
    for filename in filenames:
        check = True
        with open(filename, 'r') as file:
            data_json = json.load(file)
            for i in data_json:
                if str(message.chat.id) in i.keys():
                    check = False
        if check:
            with open(filename, 'w') as file_2:
                data_json.append({message.chat.id: []})
                json.dump(data_json, file_2, indent=4)
        else:
            pass

    # while True:
    #     current_time = datetime.datetime.now()
    #     print(current_time)
    #     if current_time.hour == 9 and current_time.minute == 0:
    #         show_all_tasks(message)
    #     time.sleep(60)


@bot.message_handler(commands=['add'])
def add_task(message):
    if message.text == '/add':
        bot.reply_to(message, text='Please write the task in format: \n '
                                   'name, deadline(01.01.2001), current/long \n'
                                   'For example: \n\n /add Make lunch, 01.12.2022, current')

    data = message.text.split(',')

    date = data[1].split('.')

    right_date = datetime.datetime(int(date[2]), int(date[1]), int(date[0]))

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

                actual_list = []

                for i in data_json:
                    if str(message.chat.id) in i.keys():
                        actual_list.append(i)
                        break
                    else:
                        pass

                if len(actual_list[0][str(message.chat.id)]) == 0:
                    task_id = 1
                else:
                    task_id = actual_list[0][str(message.chat.id)][-1]['id'] + 1

                name = data[0]
                new_task = {'Name': name[5:],
                            'Deadline': right_date.isoformat(),
                            'id': task_id
                            }

                actual_list[0][str(message.chat.id)].append(new_task)

                with open(filename, 'w') as file_2:
                    json.dump(data_json, file_2, indent=4)
                bot.reply_to(message, text='Task created successfully')
        except Exception:
            print('exception')
            pass


@bot.message_handler(commands=['current'])
def show_current_tasks(message):
    with open('data/current_tasks.json', 'r') as current_file:
        current_data = json.load(current_file)
        actual_list = []

        for i in current_data:
            if str(message.chat.id) in i.keys():
                actual_list.append(i)
                break
            else:
                pass

        sorted_data = sorted(actual_list[0][str(message.chat.id)], key=lambda d: d['Deadline'])

        for data in sorted_data:
            date = (data['Deadline'].split('T'))[0].split('-')
            view_date = date[2] + '.' + date[1] + '.' + date[0]

            result = f"Name: {data['Name']}\n" \
                     f"Deadline: {view_date}\n" \
                     f"Status: current task\n" \
                     f"id: {data['id']}\n"
            bot.send_message(message.chat.id, text=result)


@bot.message_handler(commands=['long'])
def show_long_tasks(message):
    with open('data/long_range_tasks.json', 'r') as current_file:
        current_data = json.load(current_file)
        actual_list = []

        for i in current_data:
            if str(message.chat.id) in i.keys():
                actual_list.append(i)
                break
            else:
                pass

        sorted_data = sorted(actual_list[0][str(message.chat.id)], key=lambda d: d['Deadline'])

        for data in sorted_data:
            date = (data['Deadline'].split('T'))[0].split('-')
            view_date = date[2] + '.' + date[1] + '.' + date[0]

            result = f"Name: {data['Name']}\n" \
                     f"Deadline: {view_date}\n" \
                     f"Status: long range task\n" \
                     f"id: {data['id']}\n"
            bot.send_message(message.chat.id, text=result)


@bot.message_handler(commands=['all'])
def show_all_tasks(message):
    bot.send_message(message.chat.id, text='###### CURRENT TASKS ######')
    show_current_tasks(message)

    bot.send_message(message.chat.id, text='###### LONG RANGE TASKS ######')
    show_long_tasks(message)


@bot.message_handler(commands=['delete'])
def delete_task(message):
    if message.text == '/delete':
        bot.reply_to(message, text='Please write the task in format: \n '
                                   'ID, current/long \n'
                                   'For example: \n\n /delete 13 current')

    data = message.text.split(' ')

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
            task_id = int(data[1])

            with open(filename, 'r') as file:
                data_json = json.load(file)

                for i in data_json:
                    if str(message.chat.id) in i.keys():

                        index = 0
                        for k in i[str(message.chat.id)]:
                            if k["id"] == task_id:
                                del i[str(message.chat.id)][index]

                                with open(filename, 'w') as file_2:
                                    json.dump(data_json, file_2, indent=4)
                                bot.reply_to(message, text='Task deleted successfully')
                                break
                            else:
                                index += 1
                    else:
                        pass
        except Exception:
            print('Something goes wrong')


bot.infinity_polling()
