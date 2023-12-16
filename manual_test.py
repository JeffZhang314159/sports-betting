from bs4 import BeautifulSoup
import requests

from analysis import findArbitrage
from webscraper import EventDto

def main():
    url = f'https://www.covers.com/sport/basketball/nba/linemovement/atl-at-cle/290826'
    response = requests.get(url)
    if not response.ok:
        print(f'Could not get response for {sport} {league} game {gameId} odds, skipping')
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')

    eventName = soup.find(class_='covers-OddsFlexHeading').find('h1').get_text()
    event = EventDto(eventName)

    moneylineElement = soup.find_all(id='tab-moneyline')[0]
    bookieElements = moneylineElement.find_all('table')
    for bookieElem in bookieElements:
        bookieName = bookieElem.find(class_='covers-CoversOdds-bookLogo')['alt']
        row = bookieElem.tbody.tr.find_all('td')
        time = ' '.join(row[0].div.get_text().split())
        event.bookieOdds[bookieName] = (tuple((float(td.find(class_='Decimal').get_text()) for td in row[1:])), time)

    findArbitrage(event)

if __name__ == '__main__':
    main()