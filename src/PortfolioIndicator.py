

import pandas as pd
import numpy as np




class PortfolioIndicator():

    """
    This class is used to create indicator for portfolio construction.
    The indicator indicates which portfolio the asset-date observation belongs to.
    Based on this indicator, we could group assets into different portfolios.

    """
    
    
    def __init__(self):
        
        
        pass
    
    
    def _rank(self,sub_df,var_name,number):
        """
        This function is used within the create_indicator function.
        It provides equal sized sorting on theasset based on certain sorting variable.

        :param sub_df: pd.DataFrame, the dataframe should at least contain : "ticker", "date", var_name
        :param var_name: str, the colnames of the sorting variable
        :param number: int, the number of portfolios to sort

        :return: pd.DataFrame, the dataframe contains "ticker","date" and indicator

        """
        
        indicator = pd.qcut(sub_df[var_name],q=number,labels=False,duplicates="drop")

        indicator_df = pd.concat([sub_df["date"],sub_df["ticker"],indicator],axis=1)
        
        return indicator_df
    
    
    def _top_bottom_x(self,sub_df,var_name,number):
        """
        This function is used within the create_indicator function.
        It creates three portfolios : 1. Top x 2. Bottom x 3. Middle

        :param sub_df: pd.DataFrame, the dataframe should at least contain : "ticker", "date", var_name
        :param var_name: str, the colnames of the sorting variable
        :param number: int, the x

        :return: pd.DataFrame, the dataframe contains "ticker","date" and indicator

        """
        
        indicator = pd.qcut(sub_df[var_name],q=number,labels=False,duplicates="drop")

        indicator_df = pd.concat([sub_df["date"],sub_df["ticker"],indicator],axis=1)
        
        return indicator_df
        
        sequential_series = sub_df[var_name].sort_values(ascending=True)
        
        bottom_index = list(sequential_series[0:number].index)
        top_index = list(sequential_series[-number:].index)
        
        indicator = pd.Series(np.ones(len(sequential_series)))
        indicator.index = sub_df.index
        
        indicator[top_index] = 0
        indicator[bottom_index] = 2
        
        indicator_df = pd.concat([sub_df["date"],sub_df["ticker"],indicator],axis=1)
        
        return indicator_df
        
    
    def create_rebalance_date_series(self,frequency):
        
        
        pass
    
    
    def create_indicator(self,df,var_name,rebalance_date_series,number,top_n=False):
        """
        This function is used to create indicator. It supports both equal-sized sorting
        and top/bottom X sorting. 

        It only do sorting or rebalancing on certain dates.

        :param df: pd.DataFrame, the dataframe should at least contain : "ticker", "date", var_name
        :param var_name: str, the colnames of the sorting variable
        :param number: int, the x or the number of equal sized portfolios
        :param rebalance_date_series: list(str), the str should be in dateformat
        :param top_n: boolean, whether to use top x portfolio sorting. default is to use equal sized portfolio sorting.

        :return: pd.DataFrame, the dataframe contains "ticker","date" and indicator

        """
        
        indicator_list = []
        
        for rebalance_date in rebalance_date_series:
            
            sub_df = df[df["date"] == rebalance_date]
            
            if top_n:
                
                indicator_df = self._top_bottom_x(sub_df,var_name,number)
                
            else:
                
                indicator_df = self._rank(sub_df,var_name,number)
            
            indicator_list.append(indicator_df)
        
        indicator_df = pd.concat(indicator_list,axis=0)
        
        indicator_df.columns = ["date","ticker",var_name+"_indicator"]
        
        return indicator_df
