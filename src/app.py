from loguru import logger

from binance.spot import Spot

import time
import threading
import schedule

from tools.binance_api import *
from tools.telegram_bot_api import *
from tools.super_trend import get_status
from settings import settings

api_key = settings.BINANCE_API_KEY
secret_key = settings.BINANCE_SECRET_KEY
trade_pair = 'ETHUSDT'
ticket_time = '1h'

client = Spot(key=api_key, secret=secret_key)


def trading():
    last_order = client.get_orders(trade_pair, limit=1)[0]['side']
    is_buy = True if last_order == 'BUY' else False
    logger.info(f'Последний статус: {last_order}')
    status = get_status()
    logger.info(f'Статус супертренда: {status.status}')
    current_price = get_current_ticket_price(client, trade_pair)
    logger.info(f'Текущая цена актива {trade_pair}: {current_price}')
    # data = get_ticket_time_data(client, trade_pair, ticket_time, 20)
    # trend_price = get_trend_price(data, 3)
    # is_uptrend = get_is_uptrend(data, 3)
    # Проверка на то, что цена выше тренда и тренд восходящий
    # if current_price >= trend_price and is_uptrend and not is_buy:
    if status.status == 'up' and not is_buy:
        usdt_balance = get_balance(client, 'USDT')
        buy_count = usdt_balance / current_price - 0.0001
        formated_buy_count = float("{0:.4f}".format(buy_count))
        binance_trade(client, trade_pair, 'BUY', formated_buy_count)
        log_string = f'Покупка с ценой: {current_price}, количество: {formated_buy_count}'
        logger.info(log_string)
        send_notification_to_telegram(log_string)
    elif status.status == 'down' and is_buy:
        eth_balance = get_balance(client, 'ETH')
        formated_sell_count = '{0:.4f}'.format(float("{0:.4f}".format(eth_balance)) - 0.0001)
        binance_trade(client, trade_pair, 'SELL', formated_sell_count)
        log_string = (f'Продажа с ценой: {current_price}, количество: {formated_sell_count}')
        logger.info(log_string)
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
    logger.info(f'Начало работы бота')
    schedule.every(1).minute.do(run_threaded, trading)
    schedule.every(1).day.do(run_threaded, log_day_results)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
