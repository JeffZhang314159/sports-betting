import argparse
from analysis import EventOdds
import json
import requests

SPORTS_FILE = 'sports.json'
ODDS_FILE = 'odds.json'
NCAAB_FILE = 'ncaab.txt'

# Obtain the api key that was passed in from the command line
parser = argparse.ArgumentParser(description='Sample V4')
parser.add_argument('--api-key', type=str, default='')
args = parser.parse_args()


API_KEY = args.api_key
SPORT = 'icehockey_nhl' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports
REGIONS = 'us' # uk | us | eu | au. Multiple can be specified if comma delimited
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

odds_response = requests.get(f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds', params={
    'api_key': API_KEY,
    'regions': REGIONS,
    'markets': MARKETS,
    'oddsFormat': ODDS_FORMAT,
    'dateFormat': DATE_FORMAT,
})

if odds_response.status_code != 200:
    print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')

else:
    odds_json = odds_response.json()
    for match in odds_json:
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


    print('Number of events:', len(odds_json))

    # Check the usage quota
    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    print('Used requests', odds_response.headers['x-requests-used'])