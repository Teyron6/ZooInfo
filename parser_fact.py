from bs4 import BeautifulSoup
import requests
import time
import json
import os


def create_file(folder, json_data):
    with open(f"{folder}/facts.json", "w", encoding="utf8") as json_file:
        json.dump(json_data, json_file, indent=2, ensure_ascii=False)


def get_facts(soup):
    facts = soup.find("div", class_="text").text
    facts = facts.split("\n")
    for i in facts:
        if i == "":
            facts.remove(i)
            continue

    del facts[101:110]
    return facts


def main():
    try:
        link = "https://stihi.ru/2018/11/06/1783"
        folder = "facts"
        os.makedirs(folder, exist_ok=True)
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        json_data = get_facts(soup)
        create_file(folder, json_data)

    except requests.exceptions.HTTPError:
        print("По запросу ничего не найдено")

    except requests.exceptions.ConnectTimeout:
        print("Ошибка с соединения")
        time.sleep(3)


if "__main__" == __name__:
    main()
