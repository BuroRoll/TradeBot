import numpy as np


def get_trend_price(ticket_data, deg):
    x = list(range(len(ticket_data)))
    p = np.poly1d(np.polyfit(x, ticket_data, deg))
    trend_price = p(x)[-1]
    return trend_price
