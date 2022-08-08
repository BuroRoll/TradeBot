def get_ticket_data(client, ticket, time, limit):
    data = client.klines(symbol=ticket, interval=time, limit=limit)
    result = []
    for i in data:
        average = (float(i[2]) + float(i[3])) / 2
        result.append(average)
    return result


def binance_trade(client, trade_pair, side, quantity):
    params = {
        'symbol': trade_pair,
        'side': side,
        'type': 'MARKET',
        'quantity': quantity,
    }
    client.new_order(**params)


def get_balance(client, asset, clear=False):
    account = client.account()
    free_money = 0
    for i in account['balances']:
        if i['asset'] == asset:
            free_money = i['free']
            break
    if clear:
        return float("{0:.4f}".format(free_money))
    return float("{0:.4f}".format(free_money))


def get_current_price(client, ticket):
    data = client.klines(symbol=ticket, interval='1h', limit=1)
    return data[0]
