import MetaTrader5 as mt5
from datetime import datetime
import pytz
import pandas as pd 
import matplotlib.pyplot as plt 

# initialize connections
mt5.initialize(
    path = "C:\\Users\\silin\\AppData\\Roaming\\MetaTrader 5\\terminal64.exe",
    login = 35146240,
    password = "xt7lixru"
    )

# query for forex pair
timezone = pytz.timezone("Etc/UTC")
utc_from = datetime(2020, 1, 1, tzinfo=timezone)  # create date time for the query

rates = mt5.copy_rates_from('EURUSD', mt5.TIMEFRAME_H4, datetime.today(), 10000)

# shutdown connections
mt5.shutdown()

##### work on the data #####
rates_frame = pd.DataFrame(rates)
rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')

##### Implement Order #####
def get_info(symbol):
    '''https://www.mql5.com/en/docs/integration/python_metatrader5/mt5symbolinfo_py
    '''
    # get symbol properties
    info=mt5.symbol_info(symbol)
    return info

def open_trade(action, symbol, lot, sl_points, tp_points, deviation):
    '''https://www.mql5.com/en/docs/integration/python_metatrader5/mt5ordersend_py
    '''
    # prepare the buy request structure
    symbol_info = get_info(symbol)

    if action == 'buy':
        trade_type = mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).ask
    elif action =='sell':
        trade_type = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).bid
    point = mt5.symbol_info(symbol).point

    buy_request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": trade_type,
        "price": price,
        "sl": price - sl_points * point,
        "tp": price + tp_points * point,
        "deviation": deviation,
        "magic": ea_magic_number,
        "comment": "sent by python",
        "type_time": mt5.ORDER_TIME_GTC, # good till cancelled
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    # send a trading request
    result = mt5.order_send(buy_request)        
    return result, buy_request 


def close_trade(action, buy_request, result, deviation):
    '''https://www.mql5.com/en/docs/integration/python_metatrader5/mt5ordersend_py
    '''
    # create a close request
    symbol = buy_request['symbol']
    if action == 'buy':
        trade_type = mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).ask
    elif action =='sell':
        trade_type = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).bid
    position_id=result.order
    lot = buy_request['volume']

    close_request={
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "position": position_id,
        "price": price,
        "deviation": deviation,
        "magic": ea_magic_number,
        "comment": "python script close",
        "type_time": mt5.ORDER_TIME_GTC, # good till cancelled
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    # send a close request
    result=mt5.order_send(close_request)