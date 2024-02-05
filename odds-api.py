import argparse
from datetime import date
import json
import requests

from analysis import EventDto, findArbitrage, findPlusEV

SPORTS_FILE = 'sports.json'
ODDS_FILE = 'odds.json'
NCAAB_FILE = 'ncaab.txt'

# use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports
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
REGIONS = 'us' # uk | us | eu | au. Multiple can be specified if comma delimited
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
BOOKMAKERS = ','.join(BOOKMAKERS_LIST)
MARKETS = 'h2h' # h2h | spreads | totals. Multiple can be specified if comma delimited
ODDS_FORMAT = 'decimal' # decimal | american
DATE_FORMAT = 'iso' # iso | unix

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# First get a list of in-season sports
#   The sport 'key' from the response can be used to get odds in the next request
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
"""
sports_response = requests.get('https://api.the-odds-api.com/v4/sports', params={
    'api_key': API_KEY
})

if sports_response.status_code != 200:
    print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')

else:
    with open(SPORTS_FILE, 'w') as f:
        f.write(json.dumps(sports_response.json(), indent = 2))
    print('List of in season sports:', sports_response.json())
"""


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# Now get a list of live & upcoming games for the sport you want, along with odds for different bookmakers
# This will deduct from the usage quota
# The usage quota cost = [number of markets specified] x [number of regions specified]
# For examples of usage quota costs, see https://the-odds-api.com/liveapi/guides/v4/#usage-quota-costs
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

RECORD = True

def main(api_key):
    today = date.today()
    for SPORT in SPORTS_LIST:
        odds_response = requests.get(f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds', params={
            'api_key': api_key,
            #'regions': REGIONS,
            'bookmakers': BOOKMAKERS,
            'markets': MARKETS,
            'oddsFormat': ODDS_FORMAT,
            'dateFormat': DATE_FORMAT,
        })

        if odds_response.status_code != 200:
            print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')
            continue

        odds_json = odds_response.json()

        if RECORD:
            filename = f'odds-api-data/{SPORT}_{MARKETS}_odds_{today}.json'
            with open(filename, 'w') as f:
                json.dump(odds_json, f, indent=4)

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

        print('Number of events:', len(odds_json))

        # Check the usage quota
        print('Remaining requests', odds_response.headers['x-requests-remaining'])
        print('Used requests', odds_response.headers['x-requests-used'])

if __name__ == '__main__':
    # Obtain the api key that was passed in from the command line
    parser = argparse.ArgumentParser(description='Sample V4')
    parser.add_argument('--api-key', type=str, default='')
    args = parser.parse_args()
    api_key = args.api_key
    main(api_key)