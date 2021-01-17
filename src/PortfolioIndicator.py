

import pandas as pd
import numpy as np




class PortfolioIndicator():

    """
    This class is used to create indicator for portfolio construction.
    The indicator indicates which portfolio the asset-date observation belongs to.
    Based on this indicator, we could group assets into different portfolios.

    """
    
    
    def __init__(self):

        self.initilized = True

        print("initialized.")
    
    
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

    def create_indicator_double_sort(self,df,signal_1_name,signal_2_name,rebalance_date_series,number_1,number_2):
        """
        This function is used to create indicator based on double sorting. It currently only support quantile ranking method.
        To note, the double sorting is different from simply applying ranking twice independently.

        It only do sorting or rebalancing on certain dates.

        :param df: pd.DataFrame, the dataframe should at least contain : "ticker", "date", signal_1_name, signal_2_name
        :param signal_1_name: str, the colnames of the first sorting variable
        :param signal_2_name: str, the colnames of the second sorting variable
        :param rebalance_date_series: list(str), the str should be in dateformat
        :param number_1: int, the number of equal sized portfolios based on the first indicator
        :param number_2: int, the number of equal sized portfolios based on the second indicator

        :return: pd.DataFrame, the dataframe contains "ticker","date" and two columns of indicators.

        """


    	indicator_list = []   ### create an empty indicator list used to store indicator

    	for rebalance_date in rebalance_date_series:   ### only update portfolio on the rebalance date

    		sub_df = df[df["date"]==rebalance_date]   ### extract the sub_df at one rebalance date

    		indicator_1 = self._rank(sub_df,signal_1_name,number_1)   ### apply the quantile rank using the first indicator

    		indicator_1.columns = ["date","ticker","indicator_1"]   ### rename the columns for simplicity of understanding

    		sub_df = sub_df.merge(indicator_1,on=["date","ticker"],how="left")   ### merge the indicator_1 back to the original sub_df

    		sub_df.index = sub_df["ticker"]   ### reset the index of this sub_df. This is to faciliate the ranking of second indicator

    		def qcut(x):   ### Define the rank function that is used to rank the second indicator (the function depends on the name of the second indiator and the number of portfolios)

    			indicator_2 = pd.qcut(x[signal_2_name],q=number_2,labels=False,duplicates="drop")

    			return indicator_2

    		indicator_2 = sub_df.groupby("indicator_1").apply(qcut)   ### Apply the self-defined rank function on each group of indiator 1 (wihtin each portfolio on indicator one, rank the asset using indicator 2)

    		index_df = indicator_2.index.to_frame()   ### This is to reindx the output of indicator 2
    		index_df["indicator_2"] = indicator_2
    		index_df.index = range(0,index_df.shape[0])
    		indicator_2 = index_df

    		sub_df.index = range(0,sub_df.shape[0])   ### This is to facilitate the following merge

    		sub_df = sub_df.merge(indicator_2,on=["indicator_1","ticker"],how="left")   ### merge the indicator 2 back to the origianl sub_df

    		indicator_df = sub_df[["date","ticker","indicator_1","indicator_2"]]   ### extract only the indicator columns from sub_df

    		indicator_list.append(indicator_df)   ### Append the indicator_df to the storage list

    	indicator_df = pd.concat(indicator_list,axis=0)   ### Concate all indicator_df together

    	indicator_df.columns = ["date","ticker",signal_1_name+"_indicator",signal_2_name+"_indicator"]   ### rename of the columns for facilitation.

    	return indicator_df





















