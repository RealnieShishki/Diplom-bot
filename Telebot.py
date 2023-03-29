import telebot
import sqlite3
from telebot import types

bot_token = '6002982656:AAESKvZhcvKiNsLKjGiZZjqgNKP7WZ0V73Y'

bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def start_menu(message):
    markup = types.ReplyKeyboardMarkup()
    markup.row('Узнать расценки', 'Сделать заказ самостоятельно')
    markup.row('Оставить контакты менеджеру')
    bot.reply_to(message, 'Добрый день, я помогу вам сделать заказ услугу. Наши специалисты, сильные и выносливые.',
                 reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Узнать расценки')
def price_send(message):
    with open('price.txt', 'r') as file:
        data = file.read()
    bot.send_message(message.chat.id, text=data)

@bot.message_handler(func=lambda message: message.text == 'Оставить контакты менеджеру')
def add_contact(message):
    bot.send_message(message.chat.id, 'Введите контактную информацию:')
    bot.register_next_step_handler(message, handle_user_data)

def handle_user_data(message):
    with open('contacts.txt', 'a') as file:
        file.write(message.text + '\n')
    bot.send_message(message.chat.id, 'В ближайшее время менеджер с вами свяжется')

@bot.message_handler(func=lambda message: message.text == 'Сделать заказ самостоятельно')
def add_order(message):
    def ask_work_type(message):
        nonlocal work_type
        work_type = message.text
        bot.send_message(message.chat.id, 'Требуется ли транспорт?')
        bot.register_next_step_handler(message, ask_transport)

    def ask_transport(message):
        nonlocal transport
        transport = message.text
        bot.send_message(message.chat.id, 'Ваш номер телефона?')
        bot.register_next_step_handler(message, ask_phone)

    def ask_phone(message):
        nonlocal phone
        phone = message.text

        conn = sqlite3.connect('zakazy.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO telegram_data (NAME, CONTACTS, WORK_TYPE, TRANSPORT) VALUES (?, ?, ?, ?)",
                       (message.chat.first_name, phone, work_type, transport))
        conn.commit()
        conn.close()

        bot.reply_to(message, 'Ваш заказ принят, менеджер свяжется с вами для уточнения деталей заказа')

    work_type, transport, phone = '', '', ''
    bot.send_message(message.chat.id, 'Какой тип работ вас интересует?')
    bot.register_next_step_handler(message, ask_work_type)


bot.polling()
