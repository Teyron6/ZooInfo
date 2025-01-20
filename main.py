import telebot
from telebot import types
from dotenv import load_dotenv
import os

load_dotenv()
tg_token = os.getenv('TG_TOKEN')
bot = telebot.TeleBot(tg_token)


@bot.message_handler(commands=['start'])
def start_message(message):
    star_message = 'Привет я бот ZooInfo'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    animal_of_the_day_button = types.KeyboardButton('Животное дня')
    markup.add(animal_of_the_day_button)
    bot.send_message(message.chat.id, star_message, reply_markup=markup)


@bot.message_handler(content_types='text')
def reply_to_message(message):
    if message.text == 'Животное дня':
        photo_url = '' # Ссылка на фотографию
        description = '' # Текст с описанием
        bot.send_photo(message.chat.id, caption=description, photo=open(photo_url, 'rb'))
    elif message.text.find('поиск:') != -1:
        animal = message.text[6::].strip()
        bot.send_message(message.chat.id, animal)


bot.infinity_polling()