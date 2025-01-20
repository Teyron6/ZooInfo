from bs4 import BeautifulSoup
import requests
import time
import os
import json 


def save_json_file(json_data, name_file, folder_static):
    folder = f"{folder_static}/path_json_animal"
    os.makedirs(folder, exist_ok=True)
    with open(f"{folder}/{name_file}", "w", encoding="utf8") as json_file:
        json.dump(json_data, json_file, indent=2, ensure_ascii=False)


def save_img(urls_img_animal, animal, path):
    paths_img = []
    name_animal_path = f'{path}/foto_{animal}'
    os.makedirs(name_animal_path, exist_ok=True)
    for i in range(0, len(urls_img_animal)):
        name_img = f'{name_animal_path}/{animal}_{i+1}.jpg'
        img_data = requests.get(urls_img_animal[i]).content
        with open(name_img, "wb") as handler:
            handler.write(img_data)
        paths_img.append(name_img)
    return paths_img


def get_url_img_animal(soup):
    urls_img_animal = []
    tehs_img = soup.find_all("img", class_="Article_image__I_3mF")
    for tech in tehs_img:
        urls_img_animal.append(tech['data-large-src'])
    return urls_img_animal


def main():
    try:
        animal = 'Гепард'
        folder_static = 'static'
        name_json_file = f'{animal.lower()}.json'
        url = f'https://fonwall.ru/search/{animal.lower()}/'
        params = {'catalog': 'animals'}
        os.makedirs(folder_static, exist_ok=True)
        response = requests.get(url=url, params=params)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        urls_img_animal = get_url_img_animal(soup)
        paths_img = save_img(urls_img_animal, animal.lower(), folder_static)
        save_json_file(paths_img, name_json_file, folder_static)

    except requests.exceptions.HTTPError:
        print("По запросу ничего не найдено")

    except requests.exceptions.ConnectTimeout:
        print("Ошибка с соединения")
        time.sleep(3)


if "__main__" == __name__:
    main()
