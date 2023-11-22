from collections import defaultdict
import json

# Data object to parse OddsAPI JSON data
class EventOdds:
    def __init__(self, id: str, sport_key: str, sport_title: str, commence_time: str, home_team: str, away_team: str, bookmakers: list):
        self.sport_key = sport_key
        self.sport_title = sport_title
        self.commence_time = commence_time
        self.home_team = home_team
        self.away_team = away_team

        self.h2h = defaultdict(list)

        for bookie in bookmakers:
            bookie_title = bookie['title']
            markets = bookie['markets']
            for market in markets:
                for outcome in market['outcomes']:
                    name = outcome['name']
                    price = outcome['price']
                    if market['key'] == 'h2h':
                        self.h2h[name].append((price, bookie_title))
                    else:
                        print(f"Unsupported market {market['key']} for event {self.sport_key}")                   

    def __str__(self):
        return f'{self.sport_title}: {self.home_team} v.s {self.away_team} @ {self.commence_time} has these odds: \n {dict(self.h2h)}'


ODDS_FILE = 'odds.json'

with open(ODDS_FILE, 'r') as f:
    upcoming_odds = json.load(f)
    
    for match in upcoming_odds:
        eventOdds = EventOdds(**match)
        
        print(eventOdds)
        totalImpliedOdds = 0
        for outcome, prices in eventOdds.h2h.items():
            bestPrice, bestBookie = max(prices)
            print(f'Best odds for {outcome} is {bestPrice} offered by {bestBookie}')
            totalImpliedOdds += 1 / bestPrice

        print(f'Total implied odds: {totalImpliedOdds}')
        if totalImpliedOdds < 1:
            print('Arbitrage opportunity!')
        print()


