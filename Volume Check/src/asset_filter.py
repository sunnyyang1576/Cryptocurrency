import pandas as pd 
import numpy as np 


class UniverseFilter():
    """
    This asset is used to filter out asset universe based on certain criterion.

    """
    
    def __init__(self,asset_universe):
        """
        The initialization requires a list of tickers. It would later on generate a updated asset universe.

        :param asset_universe: list(str)
        """
        
        self.asset_universe = asset_universe
        self.update_universe = asset_universe
    
    def vol_filter(self,vol_series,threshold="25%"):
        """
        This function is used to filter out the unvierse based on the transaction volume.
        It filters out the ones with volume falling below the threshold.
        It will update the attribute of update_universe.

        :param vol_series: pd.Series(float)
        :param threshold: str
        """
        
        thres_vol = vol_series.describe()[threshold]
        valid_asset = list(vol_series[vol_series>=thres_vol].index)
        
        self.update_universe = valid_asset







