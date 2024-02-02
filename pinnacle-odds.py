import requests
from bs4 import BeautifulSoup

def main():
    sportsAndLeagues = [
        ('football', 'nfl'),
        ('basketball', 'nba'),
        ('hockey', 'nhl'),
    ]

    for sport, league in sportsAndLeagues:
        upcomingGamesUrl = f'https://www.pinnacle.com/en/{sport}/{league}/matchups#period:0'
        response = requests.get(upcomingGamesUrl)
        if not response.ok:
            print(f'Could not get response for {sport} {league} upcoming games, skipping')
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup.prettify())
        table = soup.find(class_='contentBlock')
        print(table.prettify())


if __name__ == '__main__':
    main()