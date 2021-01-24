
import pandas as pd 
import numpy as np 





class SignalCreator_Momentum():
    """
    This class is used to create momentum signal.

    """
    
    
    def __init__(self,asset_universe,price_df_wide):
        """
        The initialization requires the asset universe and the price_df in pivotal table format.

        :param asset_universe: list(str)
        :param price_df_wide: pd.DataFrame, columns: ticker, index: date

        """
        
        self.asset_universe = asset_universe
        self.price_df = price_df_wide[asset_universe]
        
        
    def create_signal(self,look_back):
        """
        This function is used to create the momentum signal with certain look_back window length

        :param look_back: int

        :return: pd.Series(float)
        """
        
        signal = self.price_df.pct_change(look_back).iloc[-1,:]
        
        return signal