
import pandas as pd
import numpy as np





class PortfolioConstructor():

    """
    This function is used to calculate portfolio return time series.

    """
    
    
    def __init__(self,component_ret_df):
        """
        The initialization requires a dataframe that contains the retrun and indicator.

        :param component_ret_df: pd.DataFrame, it should at least contains 1. "date" 2. "ticker" 3. indicator 4. "ret"


        """


        
        self.return_df = component_ret_df

        self._create_year_month_day_variable()


    def _create_year_month_day_variable(self):
        """
        This function is used to create year, month and day variable.


        """

        def year(x):

            return x.year

        def month(x):

            return x.month

        def day(x):

            return x.day

        self.return_df["year"] = self.return_df["date"].apply(year)
        self.return_df["month"] = self.return_df["date"].apply(month)
        self.return_df["day"] = self.return_df["date"].apply(day)


        
    
    
    def create_portfolio_series(self,var_name,equal_weight=True,pivot_table=True):
        """
        This function groups the assets at each date based on indicator and calculate the return
        using either equal-weighted or market cap weighted method.

        :param var_name: str, the colnames of indicator
        :param equal_weight: boolean, whether to create using equal weighted or market cap weighted method
        :param pivot_table: boolean, whether to convert the result into pivotal table or not.

        :return: pd.DataFrame, portfolio return dataframe

        """
        
        def value_weighted_return(x):
            
            tot_cap = sum(x["market_cap"])
            weight = x["market_cap"]/tot_cap
            ret = sum(x["ret"]*weight)
            
            return ret
        
        def equal_weight_return(x):
            
            return_series = x["ret"]
            total_number = len(return_series)
            
            return sum(return_series/total_number) 
        
        
        df = self.return_df
        
        if equal_weight:
            
            port_df = df.groupby([var_name,"year","month","day"]).apply(equal_weight_return)
        
        else:
            
            port_df = df.groupby([var_name,"year","month","day"]).apply(value_weighted_return)
        
        
        index_df = port_df.index.to_frame()
        
        port_df = pd.concat([index_df,port_df],axis=1)
        
        port_df.index = range(0,len(port_df))
        
        
        port_df.columns = [var_name,"year","month","day","portfolio_return"]
        
        port_df["date"] = port_df["year"].astype(str) + "-" + port_df["month"].astype(str) + "-" + port_df["day"].astype(str)
        
        port_df["date"] = pd.to_datetime(port_df["date"])
        
        port_df = port_df[[var_name,"date","portfolio_return"]]
        
        
        if pivot_table:
            
            port_df = pd.pivot_table(port_df,values="portfolio_return",index=["date"],columns=[var_name])
        
        return port_df





        