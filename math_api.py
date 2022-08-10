import numpy as np


def get_trend_price(ticket_data, deg):
    x = list(range(len(ticket_data)))
    p = np.poly1d(np.polyfit(x, ticket_data, deg))
    trend_price = p(x)[-1]
    return trend_price


def get_trend_coef(ticket_data, deg):
    x = list(range(len(ticket_data)))
    p = np.poly1d(np.polyfit(x, ticket_data, deg))
    return p.coefficients[0]


def get_is_uptrend(ticket_data, deg):
    x = list(range(len(ticket_data)))
    p = np.poly1d(np.polyfit(x, ticket_data, deg))
    data = p(x)
    return data[-1] > data[-2]
