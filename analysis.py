class EventDto:
    def __init__(self, name, sport, league, market, outcomes):
        self.name = name
        self.sport = sport
        self.league = league
        self.bookieOdds = {} # Dict[str, Dict[str, float]]
        self.market = market
        self.outcomes = outcomes

def findArbitrage(eventDto):
    minimumReturn = 0.01
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
    minimumReturn = 0.01
    bankroll = 1100
    kellyCoefficient = 0.25

    model = 'Pinnacle'
    if model not in eventDto.bookieOdds:
        return
    modelOdds = eventDto.bookieOdds[model][0]
    reciprocalSum = sum((1 / price for price in modelOdds))
    fairOdds = tuple(price * reciprocalSum for price in modelOdds)

    for i in range(len(eventDto.outcomes)):
        bestPrice = max((odds[i] for (odds, _) in eventDto.bookieOdds.values()))
        bestOdds = filter(lambda x: x[1][0][i] == bestPrice, eventDto.bookieOdds.items())
        for bookie, (bookieOdds, _) in bestOdds:
            winProb = 1 / fairOdds[i]
            edge = winProb * (bookieOdds[i] - 1) - 1 + winProb
            if bookieOdds[i] > fairOdds[i] and edge > minimumReturn:
                print(f'Prices for {eventDto.outcomes[i]}: {[odds[i] for (odds, _) in eventDto.bookieOdds.values()]}')
                bankrollFraction = winProb - (1 - winProb) / (bookieOdds[i] - 1)
                wagerAmount = kellyCoefficient * bankrollFraction * bankroll
                print(f'+EV opportunity: {eventDto.name} {eventDto.sport}')
                print(f'For {eventDto.outcomes[i]} {bookie} offers {bookieOdds[i]} when fair price is {fairOdds[i]}')
                print(f'Return is {edge * 100}%. Wager {wagerAmount} on {eventDto.outcomes[i]}\n')
