import requests
import sqlite3
from selectorlib import Extractor

URL = "https://programmer100.pythonanywhere.com/tours/"


class Event:
    @staticmethod
    def scrape(url):
        """Scrape the page source from the URL"""
        response = requests.get(url)
        source = response.text
        return source

    @staticmethod
    def extract(source):
        extractor = Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"]
        return value


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("data.db")

    def store(self, text):
        row = text.split(",")
        row = [item.strip() for item in row]
        cursor = self.connection.cursor()
        cursor.execute("insert into events values(?, ?, ?)", row)
        self.connection.commit()

    def read(self, text):
        row = text.split(",")
        row = [item.strip() for item in row]
        band, city, date = row
        cursor = self.connection.cursor()
        cursor.execute("select * from events where band=? and city=? and date=?", (band, city, date))
        rows = cursor.fetchall()
        return rows


if __name__ == "__main__":
    source = Event.scrape(URL)
    extracted = Event.extract(source)
    print(extracted)

    if extracted != "No upcoming tours":
        db = Database()
        row = db.read(extracted)
        if not row:
            db.store(extracted)
