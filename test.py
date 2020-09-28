import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd 
import numpy as np

symbol = 'EURUSD'
# set up connection
mt5.initialize()
mt5.login(login = 35146240, password = "xt7lixru")

positions=mt5.positions_get(symbol = symbol)

print(positions)
print(positions == None)

x = ()