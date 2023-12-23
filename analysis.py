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

    if totalImpliedOdds < 1 / (minimumReturn + 1): # Rougly 1% return or more
        edgePercent = (1 / totalImpliedOdds - 1) * 100
        print(f'{eventDto.name} {eventDto.sport} {eventDto.league}')
        for i, offerings in enumerate(bestOfferings):
            print(f'Best prices for {eventDto.outcomes[i]} are {offerings}')
            individualArb = 1 / offerings[0][0] / totalImpliedOdds
            print(f'Bet {individualArb} on {eventDto.outcomes[i]}')
        print(f'Arbitrage opportunity! Yield = {edgePercent} %\n')