import os
from loguru import logger

from binance.spot import Spot

import time
import threading
import schedule

from binance_api import *
from math_api import *

api_key = os.getenv('API_KEY')
secret_key = os.getenv('SECRET_KEY')
trade_pair = 'ETHUSDT'
ticket_time = '1h'

client = Spot(key=api_key, secret=secret_key)


def trading():
    logger_trading = logger.bind(task='trade_result')
    last_order = client.get_orders(trade_pair, limit=1)[0]['side']
    is_buy = True if last_order == 'BUY' else False
    data = get_ticket_data(client, trade_pair, ticket_time, 20)
    current_price = data[-1]
    trend_price = get_trend_price(data, 2)
    if current_price >= trend_price and not is_buy:
        usdt_balance = get_balance(client, 'USDT')
        buy_count = usdt_balance / current_price
        formated_buy_count = "{0:.4f}".format(buy_count)
        binance_trade(client, trade_pair, 'BUY', formated_buy_count)
        logger_trading.success("Buy with current_price: {}, trend_price: {}, quantity: {}",
                               current_price, trend_price, formated_buy_count)
    elif current_price < trend_price and is_buy:
        eth_balance = get_balance(client, 'ETH')
        formated_sell_count = "{0:.4f}".format(eth_balance)
        binance_trade(client, trade_pair, 'SELL', formated_sell_count)
        logger_trading.success("Sell with current_price: {}, trend_price: {}, quantity: {}",
                               current_price, trend_price, formated_sell_count)


def log_day_results():
    logger_day_results = logger.bind(task='day_result')
    usdt_balance = get_balance(client, 'USDT', clear=True)
    if usdt_balance <= 10:
        eth_balance = get_balance(client, 'ETH', clear=True)
        eth_current_price = get_current_price(client, trade_pair)
        usdt_balance = eth_balance * eth_current_price
    logger_day_results.success('Current balance {} USD', usdt_balance)


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


def main():
    schedule.every(1).minute.do(run_threaded, trading)
    schedule.every(1).day.do(run_threaded, log_day_results)
    logger.add('./logs/day_result.log', filter=lambda record: record['extra']['task'] == 'day_result',
               format="{time:YYYY-MM-DD at HH:mm:ss} | {message}")
    logger.add('./logs/trade_result.log', filter=lambda record: record['extra']['task'] == 'trade_result',
               format="{time:YYYY-MM-DD at HH:mm:ss} | {message}")
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
