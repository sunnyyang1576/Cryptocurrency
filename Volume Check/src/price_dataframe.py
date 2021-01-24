
import pandas as pd 


class PriceDataFrame():
    """
    This class is used to organize the price dataframe from the API.

    """
    
    def __init__(self,price_df):
        """
        The initialization requires the price_df obtained from the API.

        :param price_df: pd.DataFrame, it should at least have columns of "ticker" and "time"

        """
        
        price_df["time"] = pd.to_datetime(price_df["time"])
        
        self.ori_price_df = price_df
        self.asset_universe = list(set(price_df["ticker"]))
        self.latest_time = price_df["time"].max()
    
    def create_pivot_table(self,value):
        """
        This function is used to generate the pivot table from the original price_df.

        :param value: str, it should be the colname of the value

        :return: pd.DataFrame, the column corresponds to the ticker, the index corresponds to the data index

        """
        
        pivot_table = self.ori_price_df.pivot_table(values=value,columns="ticker",index="time")
        
        return pivot_table



        