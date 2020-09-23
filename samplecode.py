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

rates = mt5.copy_rates_from('EURUSD', TIMEFRAME_H4, datetime.today(), 10000)

# shutdown connections
mt5.shutdown()

##### work on the data #####
rates_frame = pd.DataFrame(rates)
rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')

