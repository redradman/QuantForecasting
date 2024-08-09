######### import the necessary libraries
########################################
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from chronos import ChronosPipeline


# create the pipline
# pipeline = ChronosPipeline.from_pretrained(
#   "amazon/chronos-t5-base",
#   device_map="auto",
#   torch_dtype=torch.bfloat16,
# )


class ChronosModel:
    """ 
    a form of intializing chronos models that is very easy to initialize
    
    
    
    
    """
    
    # class constants 
    
    MODEL_TYPES = {"tiny": "amazon/chronos-t5-tiny", 
                   "mini": "amazon/chronos-t5-mini", 
                   "small" : "amazon/chronos-t5-small", 
                   "base" : "amazon/chronos-t5-base", 
                   "large": "amazon/chronos-t5-large"}
    
    
    
    #############################################
    def __init__(self, model: str, df, column, prediction_length: int, reserve: bool):
        
        if model not in MODEL_TYPES.keys():
            raise ValueError(f"Invalid input: '{type}'. Must be one of {MODEL_TYPES.keys()}")
        
        self.model_type = MODEL_TYPES[model]
        self.df = df
        self.prediction_length = prediction_length
        self.pipeline = ChronosPipeline.from_pretrained(
            self.model_type,
            device_map="auto",
            torch_dtype=torch.bfloat16,
            )
        
        if column not in df.columns:
            raise ValueError(f"{column} is not a column in the passed dataframe")
        
        self.column = column
        self.reserve = reserve
        
        
    #############################################
    def forecast(self):
        if self.reserve == True:
            boundary = len(df) - self.prediction_length
            context = torch.tensor(df[self.column][:boundary])          
        else:
            context = torch.tensor(df[self.column])
        forecast = pipeline.predict(context, prediction_length)
        
        
    
    #############################################
        
    def visualize(self, quantile_list = [0.1, 0.5, 0.9]):
        forecast_index = range(len(df)-prediction_length, len(df))

        low, median, high = np.quantile(forecast[0].numpy(), quantile_list, axis=0)
        
        plt.figure(figsize=(8, 4))
        plt.plot(df[self.column], color="royalblue", label="historical data")
        plt.plot(forecast_index, median, color="tomato", label="median forecast")
        plt.fill_between(forecast_index, low, high, 
                         color="tomato", 
                         alpha=0.3, 
                         label= f"{(quantile_list[-1] - quantile_list[0])* 100}% prediction interval")
        plt.legend()
        plt.grid()
        plt.show()
        