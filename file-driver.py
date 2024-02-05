from datetime import date
import json

from analysis import EventDto, findArbitrage, findPlusEV

SPORTS_LIST = [
    'americanfootball_ncaaf',
    #'americanfootball_nfl',
    'basketball_nba',
    'basketball_ncaab',
    'icehockey_nhl',
    'soccer_epl',
    'soccer_france_ligue_one',
    'soccer_germany_bundesliga',
    'soccer_italy_serie_a',
    'soccer_spain_la_liga',
    # 'soccer_usa_mls'
] 
BOOKMAKERS_LIST = [
    'pinnacle',
    'betmgm',
    'betrivers',
    'fanduel',
    'betway',
    'sport888',
    'draftkings',
    'pointsbetus',
    'betvictor',
    #'leovegas',
]
MARKETS = 'h2h' # h2h | spreads | totals. Multiple can be specified if comma delimited

def main():
    today = date.today()
    for SPORT in SPORTS_LIST:
        filename = f'odds-api-data/{SPORT}_{MARKETS}_odds_{today}.json'
        
        try:
            with open(filename, 'r') as odds_file:
                odds_json = json.load(odds_file)
        except FileNotFoundError:
            print(f'{filename} not found')
            continue

        print(f'{SPORT} has {len(odds_json)} upcoming games')
        
        for match in odds_json:
            name = f'{match["home_team"]} v.s {match["away_team"]}'
            sport = SPORT
            league = SPORT
            market = MARKETS

            if len(match['bookmakers']) == 0:
                continue
            outcomes = [outcome['name'] for outcome in match['bookmakers'][0]['markets'][0]['outcomes']]
            eventDto = EventDto(name, sport, league, market, outcomes)
            
            for bookie in match['bookmakers']:
                bookieName = bookie['title']
                time = bookie['markets'][0]['last_update']
                odds = tuple(outcome['price'] for outcome in bookie['markets'][0]['outcomes'])
                eventDto.bookieOdds[bookieName] = (odds, time) 
            
            findArbitrage(eventDto)
            findPlusEV(eventDto)

if __name__ == '__main__':
    main()