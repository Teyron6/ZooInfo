from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import os
import time
import json


def create_url(url_viki, name_animal):
    url_animal = urljoin(url_viki, name_animal)
    return url_animal


def info_animal(soup, folder, url_animal):
    # get brief information
    brief_info = (
        soup.find("div", class_="mw-content-ltr mw-parser-output")
        .find("p", recursive=False)
        .text
    )
    # get img
    img = soup.find("table").find("img", class_="mw-file-element")["src"]
    img = f"https:{img}"
    # get name
    name_animal = soup.find("span", class_="mw-page-title-main").text
    path_file = f"{folder}/{name_animal}.jpg"
    date_animal = {
        "name_animal": name_animal,
        "img_src": img,
        "brief_info": brief_info,
        "path_file": path_file,
        "url_site": url_animal,
    }
    return date_animal


def save_json_file(json_data, name_file, folder="JSON"):
    with open(f"{folder}/{name_file}.json", "w", encoding="utf8") as json_file:
        json.dump(json_data, json_file, indent=2, ensure_ascii=False)


def save_img(img_url, name_img):
    img_data = requests.get(img_url).content
    with open(name_img, "wb") as handler:
        handler.write(img_data)


def main():
    try:
        name_animal = "Бурый медведь"
        folder_static = 'static'
        folder = f"{folder_static}/viku_img_animals"
        folder_file = f"{folder_static}/viku_data_animals"

        os.makedirs(folder_static, exist_ok=True)
        os.makedirs(folder, exist_ok=True)
        os.makedirs(folder_file, exist_ok=True)

        url_viki = "https://ru.wikipedia.org/wiki/"
        url_animal = create_url(url_viki, name_animal.lower())
        response = requests.get(url_animal)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        date_animal = info_animal(soup, folder, url_animal)
        
        save_json_file(date_animal, date_animal["name_animal"], folder_file)
        save_img(date_animal["img_src"], date_animal["path_file"])

    except requests.exceptions.HTTPError:
        print("По запросу ничего не найдено")

    except requests.exceptions.ConnectTimeout:
        print("Ошибка с соединения")
        time.sleep(3)


if "__main__" == __name__:
    main()
