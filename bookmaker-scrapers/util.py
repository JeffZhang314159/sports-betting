def americanToDecimalOdds(americanOdds):
    """
        Converts from American odds format to decimal odds format, rounded to 3 decimal places
    """

    if americanOdds >= 0:
        return round(americanOdds / 100 + 1, 4)
    else:
        return round(100 / (-americanOdds) + 1, 4)