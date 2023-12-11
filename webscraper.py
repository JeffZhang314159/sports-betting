import requests
from bs4 import BeautifulSoup

class EventDto:
    def __init__(self, name):
        self.name = name
        self.bookieOdds = {}

url = "https://www.covers.com/sport/football/ncaaf/linemovement/miss-at-msst/286296"
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, "html.parser")

eventName = soup.find(class_="covers-OddsFlexHeading").find("h1").get_text()
event = EventDto(eventName)

moneylineElement = soup.find_all(id="tab-moneyline")[0]
bookieElements = moneylineElement.find_all("table")
for bookieElem in bookieElements:
    bookieName = bookieElem.find(class_="covers-CoversOdds-bookLogo")["alt"]
    row = bookieElem.tbody.tr.find_all("td")
    time = ' '.join(row[0].div.get_text().split())
    event.bookieOdds[bookieName] = (tuple((td.find(class_="Decimal").get_text() for td in row[1:])), time)

print(event.bookieOdds)