import datetime

from bs4 import BeautifulSoup
import requests
from models.appmodels import Menu, Dish
import re
import dateutil.parser

months = ["januar", "februar", "marts", "april", "maj", "juni", "juli", "august", "september", "oktober", "november", "december"]


def locationvalidator(location: str):
    if location in ['multihuset', "havremarken", "kl-verblomsten", "aastvej", "midtown", "kornmarken", "kantine-oestergade"]:
        return True
    else:
        return False



def formatDate(dateItem: str):
    day = dateItem.split(" ")[0].replace(".","").zfill(2)
    month = str(months.index(dateItem.split(" ")[1].strip())+1).zfill(2)

    return day+"-"+month


def getWeekMenu(location: str):
    menus = []

    response = requests.get(f"https://lego.isscatering.dk/{location}/da/ugemenu")
    soup = BeautifulSoup(response.text, 'html.parser')
    soup.find("div", {"id": "new-two-week-menu"})
    week_obj = soup.find("h2", {"class": "header-week"})
    menu = soup.find("div", {"class": "week-container"})
    menu_items = menu.find_all("div", {"class": "menu-row"})

    day = ""
    title = ""
    description = ""

    dates = week_obj.contents[0].strip().split(" - ")
    year = dates[1][-4:]
    from_date = dateutil.parser.parse(formatDate(dates[0])+"-"+year, dayfirst=True)
    end_date = dateutil.parser.parse(formatDate(dates[1])+"-"+year, dayfirst=True)

    dayindex = 0
    activeindex = 0
    for item in menu_items:
        newday = ""
        if item.find("h2"):
            day = item.find("h2").text.strip()
            dayindex = dayindex+1

        if item.find("div", {"class": "title"}):
            title = item.find("div", {"class": "title"}).text.strip()

        if item.find("div", {"class": "description"}):
            description = item.find("div", {"class": "description"}).text.strip()

        if day != "" and title != "" and description != "":
            dish = Dish(dish_type=title, name=description, lang="da")
            if activeindex != dayindex:
                menu = Menu(day=from_date+datetime.timedelta(days=dayindex-1), dishes=[])
                menus.append(menu)
                activeindex = dayindex
            menus[-1].dishes.append(dish)

            title = ""
            description = ""

    responseEng = requests.get(f"https://lego.isscatering.dk/{location}/en/weekmenu")
    soupEng = BeautifulSoup(responseEng.text, 'html.parser')
    soupEng.find("div", {"id": "new-two-week-menu"})
    menuEng = soupEng.find("div", {"class": "week-container"})
    menu_itemsEng = menuEng.find_all("div", {"class": "menu-row"})
    dayindex = 0
    activeindex = 0
    for item in menu_itemsEng:
        newday = ""
        if item.find("h2"):
            day = item.find("h2").text.strip()
            dayindex = dayindex + 1

        if item.find("div", {"class": "title"}):
            title = item.find("div", {"class": "title"}).text.strip()

        if item.find("div", {"class": "description"}):
            description = item.find("div", {"class": "description"}).text.strip()

        if day != "" and title != "" and description != "":
            dish = Dish(dish_type=title, name=description, lang="en")

            [x for x in menus if x.day == from_date+datetime.timedelta(days=dayindex-1)][0].dishes.append(dish)

            title = ""
            description = ""

    return menus