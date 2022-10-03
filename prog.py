import urllib, json
from bs4 import BeautifulSoup
import time
import requests
from pars import get_price


#-----------------Открытие файла статистики-------------------
def open_file():
    with open("res_data.json") as file:
        activity = json.load(file)
    return activity


#-----------------Начально определение статистики-------------------
def activity_bot(status,disc,id):
    activity = open_file()

    print(id in activity)
    if not (id in activity):
        activity[id]= {
            "condition": status,
            "discount": disc,
            "price":get_price()
            }
        with open("res_data.json", "w") as file:
            json.dump(activity, file, indent=4, ensure_ascii=False)


#-----------------Получение состояния-------------------
def set_condition(cond,id):
    activity = open_file()
    activity[id]["condition"] = cond

    with open("res_data.json", "w") as file:
        json.dump(activity, file, indent=4, ensure_ascii=False)


#-----------------Получение скидки-------------------
def set_discount(disc,id):
    activity = open_file()
    activity[id]["discount"] = disc

    with open("res_data.json", "w") as file:
        json.dump(activity, file, indent=4, ensure_ascii=False)

#-----------------Получение цены-------------------
def set_price(price,id):
    activity = open_file()
    activity[id]["price"] = price

    with open("res_data.json", "w") as file:
        json.dump(activity, file, indent=4, ensure_ascii=False)


#-----------------Отправка статистики-------------------
def get_activity(id):
    activity = open_file()
    return activity[id]

def main():

    activity_bot()


if __name__ == "__main__":
    main()
