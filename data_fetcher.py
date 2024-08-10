# importing the dependencies

from secret import *
import pandas as pd 
import ssl
from enum import Enum

# bypass certificate verification
ssl._create_default_https_context = ssl._create_unverified_context



# address of the gaurds for checking the existance of passed strings
CRYPTO_LIST = "digital_currency_list.csv"
crypto_list_df = pd.read_csv(CRYPTO_LIST)








def crypto_symbol_guard(ticker: str):
    """
    Prevents wrong spelling by checking the passed string aginst database if it does not exist returns false
    """
    if ticker.upper() in crypto_list_df.values:
        return True
    return False


class Timeframe(Enum):
    """
    An enum used for specifying timeframes and reducing errors
    """
    ONE_MINUTE = "1m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    THIRTY_MINUTES = "30m"
    ONE_HOUR = "1h"
    FOUR_HOURS = "4h"
    DAILY = "1d"
    WEEKLY = "1w"
    MONTHLY = "1mo"



# define data_fetcher class called Hermes (Greek mythology lol)
class Hermes:
    """
    Model used for getting all of the market data
    """
    
    def __init__(self):
        self.api_key = get_secret()
        self.base_url = get_base_url()
        
    def build_dataframe(symbol: str, 
                        ):
        
        
        """
        
        """
        
        
        pass
    
        
    
    
    

