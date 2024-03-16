from collections import defaultdict
from seleniumwire import webdriver
import requests
import time

from util import americanToDecimalOdds

API_KEY_HEADER = 'X-API-Key'


def get_pinnacle_api_token():
    driver = webdriver.Firefox()
    driver.get('https://www.pinnacle.com')
    time.sleep(10)
    token = ''
    for request in driver.requests:
        if API_KEY_HEADER in request.headers:
            token = request.headers[API_KEY_HEADER]

    print(token)
    driver.quit()
    return token


def clean_matchups_json(matchups_json):
    """
        Returns transforms raw matchups json to a dictionary mapping parentId's to list of matchupIds and their bet info
    """
    matchups_data = defaultdict(list)
    for match in matchups_json:
        if match['isLive']:
            continue
        
        if 'parent' not in match or match['parent'] is None:
            match_id = match['id']
            if match_id not in matchups_data:
                matchups_data[match_id] = match['participants']
        else:
            if 'participants' not in match['parent']:
                continue
                
            match_id = match['parent']['id']
            if match_id not in matchups_data:
                matchups_data[match_id] = match['parent']['participants']

    return dict(matchups_data)

leagues = {
    #493: 'NCAA Basketball',
    #487: 'NBA Basketball',
    #1456: 'NHL Hockey',
    3431: 'ATP Indian Wells Tennis'
}

def req(league_id):
    #token = get_pinnacle_api_token()
    token = 'CmX2KcMrXuFmNg6YFbmTxE0y9CIrOi0R'
    headers = {'X-API-Key': token}
    res_matchups = requests.get(f'https://guest.api.arcadia.pinnacle.com/0.1/leagues/{league_id}/matchups', headers=headers)
    res_odds = requests.get(f'https://guest.api.arcadia.pinnacle.com/0.1/leagues/{league_id}/markets/straight', headers=headers)
    
    matchups_json = res_matchups.json()
    matchups_data = clean_matchups_json(matchups_json)

    #print(matchups_json)

    odds_json = res_odds.json()
    # Look at odds data primarily.
    for oddsItem in odds_json:
        if oddsItem['period'] != 0 or oddsItem['matchupId'] not in matchups_data:
            #print(oddsItem)
            continue

        match_id = oddsItem['matchupId']
        teams = list(map(lambda x: x['name'], matchups_data[match_id]))
        
        if oddsItem['type'] == 'total':
            sides = [item['designation'] for item in oddsItem['prices']]
        else:
            sides = teams

        prices = [americanToDecimalOdds(item['price']) for item in oddsItem['prices']]
        reciprocal_sum = sum((1 / price) for price in prices)
        fair_prices = [price * reciprocal_sum for price in prices]

        print(f"{' vs '.join(teams)} {oddsItem['type']}")

        if oddsItem['type'] == 'moneyline':
            for team, fair_price in zip(sides, fair_prices):
                print(f"{team}: {fair_price}")
        elif oddsItem['type'] == 'total' or oddsItem['type'] == 'spread':
            for i, (team, fair_price) in enumerate(zip(sides, fair_prices)):
                points = oddsItem['prices'][i]['points']
                print(f"{team} {points}: {fair_price}")
        print()
    

if __name__ == '__main__':
    for league_id, name in leagues.items():
        print(name)
        req(league_id)