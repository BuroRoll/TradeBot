def get_ticket_time_data(client, ticket, time, limit):
    data = client.klines(symbol=ticket, interval=time, limit=limit)
    result = []
    for i in data:
        average = (float(i[2]) + float(i[3])) / 2
        result.append(average)
    return result


def get_current_ticket_price(client, ticket):
    return client.ticker_price(ticket)['price']


def binance_trade(client, trade_pair, side, quantity):
    params = {
        'symbol': trade_pair,
        'side': side,
        'type': 'MARKET',
        'quantity': quantity,
    }
    client.new_order(**params)


def get_balance(client, asset):
    account = client.account()
    free_money = 0
    for i in account['balances']:
        if i['asset'] == asset:
            free_money = i['free']
            break
    return float(free_money)
