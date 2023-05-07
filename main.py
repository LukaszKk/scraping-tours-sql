import requests
import sqlite3
from selectorlib import Extractor

URL = "https://programmer100.pythonanywhere.com/tours/"

connection = sqlite3.connect("data.db")


def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    extractor = Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def store(text):
    row = text.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("insert into events values(?, ?, ?)", row)
    connection.commit()


def read(text):
    row = text.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("select * from events where band=? and city=? and date=?", (band, city, date))
    rows = cursor.fetchall()
    return rows


if __name__ == "__main__":
    source = scrape(URL)
    extracted = extract(source)
    print(extracted)

    if extracted != "No upcoming tours":
        row = read(extracted)
        if not row:
            store(extracted)
