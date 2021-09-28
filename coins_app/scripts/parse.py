"""
Module with parsing functions
"""

import os
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from coins.models import Coin
from django.conf import settings

SOURCE = 'https://www.ua-coins.info'
NOT_PRECIOUS = SOURCE + '/catalog/base/all'
HEADER = {
    "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" +
        "AppleWebKit/537.36 (KHTML, like Gecko)" +
        "Chrome/83.0.4103.116" +
        "Safari/537.36",
}

DATE_FORMAT = "%d.%m.%Y"
TODAY = datetime.now().strftime(DATE_FORMAT)


def add_coin(coin_row: BeautifulSoup.element.Tag) -> None:
    """
    Function for parsing coin data, such as weight, series, images etc.

    Parameters
    ----------
    coin_row : BeautifulSoup.element.Tag
        Row  with coin data from main table with coins list
    """
    title = coin_row.a.text
    year = int(coin_row.td.text[-4:])
    coin = Coin.get(title, year)

    # Search and clean price
    price = re.sub(r'\D', '', coin_row.find("td", {"data-title": f"Цена {TODAY}"}).text)

    if coin is None:
        url = SOURCE + coin_row.a.get("href")
        response = requests.get(url, headers=HEADER)

        if response.status_code == 200:
            page = BeautifulSoup(response.text, "lxml")

            # ['Release date', 'Nominal', 'Metal', 'Weight', 'Diameter', 'Circulation']
            info = list(
                map(lambda x: x.text,
                    page.find('table', {'class': 'coin-info'}).findAll('tr')[1].findAll('td'))
            )

            release_date = datetime.strptime(info[0], DATE_FORMAT).date()
            nominal = int(info[1])
            metal = info[2]
            weight = float(info[3])
            diameter = float(info[4])
            circulation = ''.join(filter(lambda x: x.isdigit(), info[5]))
            series = page.find('div', {'class': 'category'}).a.text
            price = int(price) if price.isdigit() else 0

            # Search for obverse and reverse urls
            obverse, reverse = None, None
            for img in page.findAll("img"):
                if img.get("alt"):
                    if obverse is None and "Аверс" in img["alt"]:
                        obverse = SOURCE + img["src"]
                    if reverse is None and "Реверс" in img["alt"]:
                        reverse = SOURCE + img["src"]

            coin = Coin(title=title,
                        release_date=release_date,
                        nominal=nominal,
                        series=series,
                        circulation=circulation,
                        metal=metal,
                        weight=weight,
                        diameter=diameter,
                        price=price)
            coin.save()

            coin.obverse = os.path.join("coins_obverse", f"obverse_{coin.pk}.jpg")
            coin.reverse = os.path.join("coins_reverse", f"reverse_{coin.pk}.jpg")

            # Saving obverse and reverse images
            with open(os.path.join(settings.MEDIA_ROOT, str(coin.obverse)), 'wb') as file:
                file.write(requests.get(obverse, headers=HEADER).content)
            with open(os.path.join(settings.MEDIA_ROOT, str(coin.reverse)), 'wb') as file:
                file.write(requests.get(reverse, headers=HEADER).content)

            coin.save()
        else:
            print(f"Bad status code: {response.status_code}")


def update_prices(add_new: bool = True) -> None:
    """
    Function for parsing list of coins and their prices.

    Parameters
    ----------
    add_new : bool
        Checkbox for adding new coins, optional, True for default
    """
    response = requests.get(NOT_PRECIOUS, headers=HEADER)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")

        # We delete header and footer and start from bottom
        for coin_row in soup.table.find_all(["tr"])[-1:1:-1]:
            print(type(coin_row))
            # If we have row with coin data
            if len(coin_row.find_all(["td"])) == 5 and coin_row.a.text:
                title = coin_row.a.text
                year = int(coin_row.td.text[-4:])

                coin = Coin.get(title, year)

                if coin is None:
                    if add_new:
                        add_coin(coin_row)
                else:
                    # Search and clean price
                    new_price = re.sub(r'\D', '', coin_row.find('td', {'data-title': f'Цена {TODAY}'}).text)

                    if new_price.isdigit():
                        new_price = int(new_price)
                    else:
                        new_price = 0

                    coin.price = new_price
                    coin.save()
    else:
        print(f"Bad status code: {response.status_code}")


def run():
    """
    Start point
    """
    update_prices()
