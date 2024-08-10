# importing the dependencies

from secret import *
import pandas as pd 
import ssl

# bypass certificate verification
ssl._create_default_https_context = ssl._create_unverified_context




# define class
class Hermes:
    """
    Model used for getting all of the market data
    """
    
    def __init__(self):
        self.api_key = get_secret()
        self.base_url = get_base_url()
    
        
    
    
    

