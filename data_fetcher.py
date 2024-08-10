# importing the dependencies

from secret import *
import pandas as pd 
import ssl
from typing import List
from urllib.parse import urlencode, urlunparse



##################################### SETTING UP 
################################################
# bypass certificate verification
ssl._create_default_https_context = ssl._create_unverified_context



# address of the gaurds for checking the existance of passed strings
CRYPTO_LIST = "digital_currency_list.csv"
crypto_list_df = pd.read_csv(CRYPTO_LIST)


# note the timefrmae dict below the values ending in m are parameters while D,M,W have their associated functions as values 

TIMEFRAME_DICT = {"1min": "CRYPTO_INTRADAY", 
                    "5min": "CRYPTO_INTRADAY", 
                    "15min":"CRYPTO_INTRADAY", 
                    "30min": "CRYPTO_INTRADAY", 
                    "60min": "CRYPTO_INTRADAY", 
                    "D": "DIGITAL_CURRENCY_DAILY",
                    "W": "DIGITAL_CURRENCY_WEEKLY",
                    "M": "DIGITAL_CURRENCY_MONTHLY"}


# list of all of the avialable indicators
INDICATOR_LIST = ['SMA', 'EMA', 'WMA', 'DEMA', 'TEMA', 'TRIMA', 'KAMA', 
                  'MAMA', 'VWAP', 'T3', 'MACD', 'MACDEXT', 'STOCH', 
                  'STOCHF', 'RSI', 'STOCHRSI', 'WILLR', 'ADX', 
                  'ADXR', 'APO', 'PPO', 'MOM', 'BOP', 'CCI', 'CMO', 
                  'ROC', 'ROCR', 'AROON', 'AROONOSC', 'MFI', 'TRIX', 
                  'ULTOSC', 'DX', 'MINUS_DI', 'PLUS_DI', 'MINUS_DM', 
                  'PLUS_DM', 'BBANDS', 'MIDPOINT', 'MIDPRICE', 'SAR', 
                  'TRANGE', 'ATR', 'NATR', 'AD', 'ADOSC', 'OBV', 
                  'HT_TRENDLINE', 'HT_SINE', 'HT_TRENDMODE', 
                  'HT_DCPERIOD', 'HT_DCPHASE', 'HT_PHASOR']

################################################





def crypto_symbol_guard(ticker: str):
    """
    Prevents wrong spelling by checking the passed string aginst database if it does not exist returns false
    """
    if ticker.upper() in crypto_list_df.values:
        return True
    return False






def build_url(base_url, path='', params=None):
    query_string = urlencode(params) if params else ''
    return urlunparse((
        'https',          # scheme
        base_url,         # netloc
        path,             # path
        '',               # params (not query params)
        query_string,     # query
        ''                # fragment
    ))

# # Example usage
# base_url = 'example.com'
# path = 'search'
# params = {
#     'q': 'python url building',
#     'page': 2
# }





# define data_fetcher class called Hermes (Greek mythology lol)
class Hermes:
    """
    Model used for getting all of the market data
    """
    
    def __init__(self):
        self.api_key = get_secret()
        self.base_url = get_base_url()
        
        
    def build_url(self, params=None, path=''):
        query_string = urlencode(params) if params else ''
        return urlunparse((
            'https',          # scheme
            self.base_url,    # netloc
            path,             # path
            '',               # params (not query params)
            query_string,     # query
            ''                # fragment
        ))

        # build_url(get_base_url(), params = {'apikey':get_secret(),
        #                                 'function' : 'DIGITAL_CURRENCY_DAILY',
        #                                 'symbol':'BTC',
        #                                 'datatype' : 'csv'})
        
    def fetch_url_with_csv_datatype(self, url: str):
        df = pd.read_csv(url)
        return df
        
    def build_dataframe(self, symbol: str, 
                        timeframe: str,
                        indicator_list: List[dict],
                        market= "USD"):
        """
        creates a comprehensive dataframe based on the timeframe for given symbol with the indicator list.
        """
        # making sure that symbol is upper case
        symbol = symbol.upper()
        # guard for symbol
        if symbol not in crypto_list_df["currency_code"].values:
            raise ValueError(f"Passed symbol is not on the list of cryptocurrencies. Modify entry")
        
        # guard for timeframe
        if timeframe not in TIMEFRAME_DICT.keys():
            raise ValueError(f"Passed timeframe value is incorrect. Must be one of {TIMEFRAME_DICT.keys()}")
        
        
        # determine the fuctions and build the params
        function = TIMEFRAME_DICT[timeframe]
        if function == "CRYPTO_INTRADAY":
            params = {'function':function,
                      'symbol': symbol,
                      'market' : market,
                      'interval' : timeframe,
                      'outputsize' : 'full',
                      'datatype' : 'csv',
                      'apikey': self.api_key}
        else: 
            params = {'function':function,
                      'symbol': symbol,
                      'market' : market,
                      'datatype' : 'csv',
                      'apikey': self.api_key}
            
        url = self.build_url(params = params)
        print(url)
        price_df = self.fetch_url_with_csv_datatype(url)
            
            
        return price_df
