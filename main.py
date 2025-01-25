import random
from telebot import TeleBot, types
from dotenv import load_dotenv
import os
import parser_viku
import parser_foto_animal
import requests
from bs4 import BeautifulSoup
import time
import threading
import schedule
import json


# Загружаем токен из .env
load_dotenv()
tg_token = os.getenv("TG_TOKEN")
bot = TeleBot(tg_token)  # Инициализируем бота

# Обьявляем переменные
animals_path = "./static/viku_data_animals"
chat_ids_file = "./static/chat_ids.json"
facts_file = "./static/facts_animals/facts.json"


def load_chat_ids():
    # Загружаем список пользователей из ./static/chat_ids.json
    if os.path.exists(chat_ids_file):
        if os.path.getsize(chat_ids_file) > 0:  # Проверяем, что файл не пустой
            with open(chat_ids_file, "r", encoding="utf-8") as file:
                return json.load(file)
        else:
            print("Файл chat_ids.json пуст. Возвращаем пустой список.")
            return []  # Если файл пуст
    return []  # Если файла не существует


def save_chat_ids(chat_ids):
    # Сохраняем пользователей в ./static/chat_ids.json
    with open(chat_ids_file, "w", encoding="utf-8") as file:
        json.dump(chat_ids, file)


def select_daily_animal():
    # Выбираем случайное животное
    global daily_animal
    random_file_path = os.path.join(
        animals_path, random.choice(os.listdir(animals_path))
    )
    with open(random_file_path, "r", encoding="utf-8") as file:
        daily_animal = json.load(file)
    print(f"Животное дня выбрано: {daily_animal['name_animal']}")


def send_animal_of_the_day(whom="all"):
    try:
        # Проверяем выбрано ли животное дня
        if daily_animal is None:
            print("Животное дня не выбрано.")
            return

        if whom == "all":
            # Отправляем животное дня в каждый чат
            for chat_id in chat_ids:
                try:
                    bot.send_photo(
                        chat_id,
                        caption=f"Сегодняшнее животное дня это: {daily_animal['name_animal']}\n\n{daily_animal['brief_info']}",
                        photo=daily_animal["img_src"],
                    )
                    print(
                        f"Животное дня отправлено в чат {chat_id}: {daily_animal['name_animal']}"
                    )
                except Exception as e:
                    print(f"Ошибка при отправке в чат {chat_id}: {e}")
        else:
            # Отправляем животное дня в определенный чат
            try:
                bot.send_photo(
                    whom,
                    caption=f"Сегодняшнее животное дня это: {daily_animal['name_animal']}\n\n{daily_animal['brief_info']}",
                    photo=daily_animal["img_src"],
                )
                print(
                    f"Животное дня отправлено в чат {whom}: {daily_animal['name_animal']}"
                )
            except Exception as e:
                print(f"Ошибка при отправке в чат {chat_id}: {e}")
    except Exception as e:
        print(f"Ошибка при отправке животного дня: {e}")


def schedule_animal_of_the_day(send_time="15:00"):
    schedule.every().day.at("00:00").do(
        select_daily_animal
    )  # Выбираем животное дня в полночь
    schedule.every().day.at(send_time).do(
        send_animal_of_the_day
    )  # Отправляем в указанное время

    # Запускаем планировщик в отдельном потоке
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)

    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()


# Комманда /start
@bot.message_handler(commands=["start"])
def start_message(message):
    global chat_ids  # Указываем что работаем с глобальной переменной

    # Проверяем есть ли пользователь в базе, если нет, заносим
    if message.chat.id not in chat_ids:
        chat_ids.append(message.chat.id)
        save_chat_ids(chat_ids)

    star_message = "Привет я бот ZooInfo"  # Переменная со стартовым сообщением
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )  # Инициилизируем клавиатуру

    # Создаем кнопки
    animal_of_the_day_button = types.KeyboardButton("Животное дня")
    finder = types.KeyboardButton("Поиск")
    random_animal = types.KeyboardButton("Случайное животное")
    random_fact = types.KeyboardButton("Случайный факт")
    photo_findef = types.KeyboardButton("Поиск фото")
    markup.add(
        animal_of_the_day_button, finder, random_animal, random_fact, photo_findef
    )  # Создаем клавиатуру

    bot.send_message(
        message.chat.id, star_message, reply_markup=markup
    )  # Отправляем стартовое сообщение


# Ответ на определенные сообщения
@bot.message_handler(content_types="text")
def reply_to_message(message):
    if message.text == "Случайное животное":
        random_file_path = os.path.join(
            animals_path, random.choice(os.listdir(animals_path))
        )
        with open(random_file_path, "r", encoding="utf-8") as file:
            random_animal = json.load(file)
        bot.send_photo(
            message.chat.id,
            caption=random_animal["brief_info"],
            photo=random_animal["img_src"],
        )

    elif message.text == "Животное дня":
        send_animal_of_the_day(message.chat.id)

    elif message.text == "Случайный факт":
        with open(facts_file, "r", encoding="utf-8") as file:
            random_fact = random.choice(json.load(file))
        bot.send_message(message.chat.id, f"Случайный факт: {random_fact}")

    elif message.text == "Поиск":
        bot.send_message(
            message.chat.id,
            "Что бы найти определенное животное напишите:\nПоиск: животное",
        )

    elif message.text == "Поиск фото":
        bot.send_message(
            message.chat.id,
            "Для того что бы найти фотографии животного напишите:\nПоиск фото: животное",
        )

    elif message.text.lower().find("поиск:") != -1:
        try:
            name_animal = message.text[6::]
            folder_static = "static"
            folder = f"{folder_static}/viku_img_animals"
            folder_file = f"{folder_static}/viku_data_animals"

            os.makedirs(folder_static, exist_ok=True)
            os.makedirs(folder, exist_ok=True)
            os.makedirs(folder_file, exist_ok=True)

            url_wiki = "https://ru.wikipedia.org/wiki/"
            url_animal = parser_viku.create_url(url_wiki, name_animal.lower())
            response = requests.get(url_animal)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "lxml")
            date_animal = parser_viku.info_animal(soup, folder, url_animal)

            parser_viku.save_json_file(
                date_animal, date_animal["name_animal"], folder_file
            )
            parser_viku.save_img(date_animal["img_src"], date_animal["path_file"])
            bot.send_photo(
                message.chat.id,
                photo=date_animal["img_src"],
                caption=f'{date_animal["name_animal"]}\n\n{date_animal["brief_info"]}',
            )

        except requests.exceptions.HTTPError:
            bot.send_message(
                message.chat.id,
                "По запросу ничего не найдено, возможно в запросе есть грамотическая ошибка",
            )

        except requests.exceptions.ConnectTimeout:
            bot.send_message(
                message.chat.id, "Ошибка с соеденением, попробуйте еще раз"
            )
            time.sleep(3)

    elif message.text.lower().find("поиск фото:") != -1:
        try:
            animal = message.text[11::].strip()
            folder_static = "static"
            name_json_file = f"{animal.lower()}.json"
            url = f"https://fonwall.ru/search/{animal.lower()}/"
            params = {"catalog": "animals"}
            os.makedirs(folder_static, exist_ok=True)
            response = requests.get(url=url, params=params)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "lxml")
            urls_img_animal = parser_foto_animal.get_url_img_animal(soup)
            paths_img = parser_foto_animal.save_img(
                urls_img_animal, animal.lower(), folder_static
            )
            parser_foto_animal.save_json_file(paths_img, name_json_file, folder_static)

            with open(
                f"./static/path_json_animal/{name_json_file}", "r", encoding="utf-8"
            ) as file:
                photos_list = json.load(file)

            media = [
                types.InputMediaPhoto(open(photo_path, "rb"))
                for photo_path in photos_list[:9]
            ]
            bot.send_media_group(message.chat.id, media=media)

        except requests.exceptions.HTTPError:
            bot.send_message(
                message.chat.id,
                "По запросу ничего не найдено, возможно в запросе есть граматическая ошибка",
            )

        except requests.exceptions.ConnectTimeout:
            bot.send_message(message.chat.id, "Ошибка с соединением")
            time.sleep(3)


chat_ids = load_chat_ids()
select_daily_animal()  # Выбираем стартовое животное дня
schedule_animal_of_the_day(
    send_time="05:14"
)  # Отправляем животное дня в определенное время
bot.polling()  # Запускаем бота
