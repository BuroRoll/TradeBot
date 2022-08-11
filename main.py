from loguru import logger

from binance.spot import Spot

import time
import threading
import schedule

from binance_api import *
from math_api import *
from telegram_bot_api import *

api_key = os.getenv('API_KEY')
secret_key = os.getenv('SECRET_KEY')
trade_pair = 'ETHUSDT'
ticket_time = '1h'

client = Spot(key=api_key, secret=secret_key)


def trading():
    logger_trading = logger.bind(task='trade_result')
    last_order = client.get_orders(trade_pair, limit=1)[0]['side']
    is_buy = True if last_order == 'BUY' else False
    data = get_ticket_time_data(client, trade_pair, ticket_time, 20)
    current_price = get_current_ticket_price(client, trade_pair)
    trend_price = get_trend_price(data, 3)
    is_uptrend = get_is_uptrend(data, 3)

    # Проверка на то, что цена выше тренда и тренд восходящий
    if current_price >= trend_price and is_uptrend and not is_buy:
        usdt_balance = get_balance(client, 'USDT')
        buy_count = usdt_balance / current_price - 0.0001
        formated_buy_count = float("{0:.4f}".format(buy_count))
        binance_trade(client, trade_pair, 'BUY', formated_buy_count)
        log_string = (
            f"Buy with current_price: {current_price}, trend_price: {trend_price}, quantity: {formated_buy_count}")
        logger_trading.success(log_string)
        send_notification_to_telegram(log_string)
    elif current_price < trend_price and is_buy:
        eth_balance = get_balance(client, 'ETH')
        formated_sell_count = '{0:.4f}'.format(float("{0:.4f}".format(eth_balance)) - 0.0001)
        binance_trade(client, trade_pair, 'SELL', formated_sell_count)
        log_string = (
            f"Sell with current_price: {current_price}, trend_price: {trend_price}, quantity: {formated_sell_count}")
        logger_trading.success(log_string)
        send_notification_to_telegram(log_string)


def log_day_results():
    logger_day_results = logger.bind(task='day_result')
    usdt_balance = get_balance(client, 'USDT')
    if usdt_balance <= 10:
        eth_balance = get_balance(client, 'ETH')
        eth_current_price = get_current_ticket_price(client, trade_pair)
        usdt_balance = eth_balance * eth_current_price
    log_string = f'Current balance {usdt_balance} USD'
    logger_day_results.success(log_string)
    send_notification_to_telegram('Daily result:')
    send_notification_to_telegram(log_string)


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
