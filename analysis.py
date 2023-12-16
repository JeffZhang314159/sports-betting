def findArbitrage(eventDto):
    totalImpliedOdds = 0

    bestOfferings = []
    for i in range(2):
        bestBookie, bestOdds = max(eventDto.bookieOdds.items(), key=lambda x: x[1][0][i])
        bestPrice = bestOdds[0][i]
        bestOfferings.append((bestPrice, bestBookie))
        totalImpliedOdds += 1 / bestPrice

    if totalImpliedOdds < 1:
        edgePercent = (1 / totalImpliedOdds - 1) * 100
        print(eventDto.name)
        for i, (bestPrice, bestBookie) in enumerate(bestOfferings):
            print(f'Best price for {i} is {bestPrice} offered by {bestBookie}')
        print(f'Arbitrage opportunity! Yield = {edgePercent} %\n')