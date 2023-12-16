import requests
from bs4 import BeautifulSoup

from analysis import findArbitrage

class EventDto:
    def __init__(self, name):
        self.name = name
        self.bookieOdds = {}

def main():
    sportsAndLeagues = [
        #('football', 'nfl'),
        #('football', 'ncaaf'),
        #('football', 'cfl'),
        ('basketball', 'nba'),
        ('basketball', 'ncaab'),
        ('basketball', 'wnba'),
        ('baseball', 'mlb'),
        ('hockey', 'nhl'),
        ('golf', 'pga'),
        ('soccer', 'mls'),
        ('soccer', 'bundesliga'),
        ('soccer', 'champions-league'),
        ('soccer', 'europa-league'),
        ('soccer', 'serie-a'),
        ('soccer', 'la-liga'),
        ('soccer', 'ligue-1'),
        ('soccer', 'premier-league'),
        ('mma', 'ufc')
    ]

    for sport, league in sportsAndLeagues:
        upcomingGamesUrl = f'https://www.covers.com/sport/{sport}/{league}/odds'
        response = requests.get(upcomingGamesUrl)
        if not response.ok:
            print(f'Could not get response for {sport} {league} upcoming games, skipping')
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        gameColumn = soup.find(class_='games-tbody')
        if not gameColumn:
            print(f'{sport} {league} has no upcoming games')
            continue

        gameIds = [element['data-game'] for element in gameColumn.find_all(class_='lineHistoryBrick')]
        
        for gameId in gameIds:
            url = f'https://www.covers.com/sport/{sport}/{league}/linemovement/whatever/{gameId}'
            response = requests.get(url)
            if not response.ok:
                print(f'Could not get response for {sport} {league} game {gameId} odds, skipping')
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            eventName = soup.find(class_='covers-OddsFlexHeading').find('h1').get_text()
            event = EventDto(eventName)

            moneylineElement = soup.find_all(id='tab-moneyline')[0]
            bookieElements = moneylineElement.find_all('table')
            for bookieElem in bookieElements:
                bookieName = bookieElem.find(class_='covers-CoversOdds-bookLogo')['alt']
                rowElem = bookieElem.tbody.tr
                if not rowElem:
                    continue
                row = rowElem.find_all('td')
                time = ' '.join(row[0].div.get_text().split())
                event.bookieOdds[bookieName] = (tuple((float(td.find(class_='Decimal').get_text()) for td in row[1:])), time)

            findArbitrage(event)

if __name__ == '__main__':
    main()
