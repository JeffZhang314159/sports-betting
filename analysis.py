def findArbitrage(eventDto):
    totalImpliedOdds = 0

    bestOfferings = []
    for i in range(len(eventDto.outcomes)):
        if not eventDto.bookieOdds.items():
            return
        
        sortedByOdds = sorted([(odds[i], bookie) for (bookie, (odds, _)) in eventDto.bookieOdds.items()], reverse=True)
        #print(sortedByOdds)
        bestOfferings.append(sortedByOdds)
        totalImpliedOdds += 1 / sortedByOdds[0][0]

    if totalImpliedOdds < 0.95: # Rougly 5 % return or more
        edgePercent = (1 / totalImpliedOdds - 1) * 100
        print(f'{eventDto.name} {eventDto.sport} {eventDto.league}')
        for i, offerings in enumerate(bestOfferings):
            print(f'Best prices for {eventDto.outcomes[i]} are {offerings}')
        print(f'Arbitrage opportunity! Yield = {edgePercent} %\n')