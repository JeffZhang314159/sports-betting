class EventDto:
    def __init__(self, name, sport, league, market, outcomes):
        self.name = name
        self.sport = sport
        self.league = league
        self.bookieOdds = {}
        self.market = market
        self.outcomes = outcomes

def findArbitrage(eventDto):
    minimumReturn = 0.0
    totalImpliedOdds = 0

    bestOfferings = []
    for i in range(len(eventDto.outcomes)):
        if not eventDto.bookieOdds.items():
            return
        
        sortedByOdds = sorted([(odds[i], bookie) for (bookie, (odds, _)) in eventDto.bookieOdds.items()], reverse=True)
        #print(sortedByOdds)
        bestOfferings.append(sortedByOdds)
        totalImpliedOdds += 1 / sortedByOdds[0][0]

    if totalImpliedOdds < 1 / (minimumReturn + 1):
        edgePercent = (1 / totalImpliedOdds - 1) * 100
        print(f'{eventDto.name} {eventDto.sport} {eventDto.league} {eventDto.market}')
        for i, offerings in enumerate(bestOfferings):
            print(f'Best prices for {eventDto.outcomes[i]} are {offerings}')
            individualArb = 1 / offerings[0][0] / totalImpliedOdds
            print(f'Bet {individualArb} on {eventDto.outcomes[i]}')
        print(f'Arbitrage opportunity! Yield = {edgePercent} %\n')

def findPlusEV(eventDto):
    minimumReturn = 0.0
    model = 'Pinnacle'
    if model not in eventDto.bookieOdds:
        return
    modelOdds = eventDto.bookieOdds[model][0]
    reciprocalSum = sum((1 / price for price in modelOdds))
    fairOdds = tuple(price * reciprocalSum for price in modelOdds)

    for bookie, (bookieOdds, _) in eventDto.bookieOdds.items():
        for i in range(len(fairOdds)):
            edge = 1 / fairOdds[i] * (bookieOdds[i] - 1) - 1 + 1 / fairOdds[i]
            if bookieOdds[i] > fairOdds[i]:
                print(f'+EV opportunity: {eventDto.name} {eventDto.sport}')
                print(f'For {eventDto.outcomes[i]} {bookie} offers {bookieOdds[i]} when fair price is {fairOdds[i]}')
                print(f'Return is {edge * 100}%')

