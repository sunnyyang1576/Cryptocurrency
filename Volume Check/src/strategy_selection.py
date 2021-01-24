
import pandas as pd 




class Strategy():
    """
    This class is used select top and bottom x assets based on certain signal or signals.

    """

    def __init__(self,asset_universe=None):
        """
        The initialization does not require anything.

        """
        
        self.asset_universe = asset_universe
    
    def topn_single_signal_selection(self,signal,n):
        """
        This function is used to find the top and bottom n asset based on the single signal.

        :param signal: pd.Series(float), index is asset ticker
        :param n: int

        :return: tuple(list(str),list(str))
        """
        
        top_portfolio = list(signal.nlargest(n).index)
        bottom_portfolio = list(signal.nsmallest(n).index)
        
        return (top_portfolio,bottom_portfolio)
    
    def topn_double_signal_selection(self,signal_1,signal_2,n_1=20,n_2=10):
        """
        This function is used to find the top and bottom n assets based on two signals.
        The assets are firstly filtered based on signal_1. 
        Then within the portfolios selected by signal_1, the signal_2 is applied.

        :param signal_1: pd.Series(float), index is asset ticker
        :param signal_2: pd.Series(float), index is asset ticker
        :param n_1: int
        :param n_2: int

        :return: tuple(list(str),list(str))

        """
        
        top_portfolio_1 = list(signal_1.nlargest(n_1).index)
        bottom_portfolio_1 = list(signal_1.nsmallest(n_1).index)
        
        top_portfolio_2 = list(signal_2[top_portfolio_1].nlargest(n_2).index)
        bottom_portfolio_2 = list(signal_2[bottom_portfolio_1].nsmallest(n_2).index)
        
        return (top_portfolio_2,bottom_portfolio_2)