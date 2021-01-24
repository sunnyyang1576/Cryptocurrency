
import pandas as pd 
import numpy as np


class OrderCreator():
    """
    This class is used to create order information. The order information should be passed to
    the order execution class.

    """
    
    def __init__(self,asset_list):
        """
        The initialization requires a list of assets that need to send order of.


        :param asset_list: list(str), list of asset ticker
        """
        
        self.asset_list = asset_list
        self.weight = None
        
    def equal_weight(self):
        """
        This function is used to create the weight of each asset based on equal weighted method.
        It then updates the weight attribute.

        """
        
        tot_num_asset = len(self.asset_list)
        
        weight = np.ones(tot_num_asset)/tot_num_asset
        
        self.weight = weight
        
    
    def weighted_weight(self,weight_series):
        """
        This function is used to create the weight of each asset based on weight series.
        The weight series should corresponds to the number of assets available.
        The weight_series does not have to sum to 1. 
        The higher the value, the higher the weight.
        It then updates the weight attribute.

        :param weight_series: list(float)


        """
        
        weight_series = np.array(weight_series)
        
        weight = weight_series/sum(weight_series)
        
        self.weight = weight

    def create_order_dictionary(self):
        """
        This function is used to generate the order dictionary. This dictionary is sent
        to the order execution module.


        :return: dict

        """
        
        if self.weight is None:
            print("No weight is assigned.")
        
        return {"asset_list":self.asset_list,"weight":self.weight,"asset_weight_list":zip(self.asset_list,self.weight)}
