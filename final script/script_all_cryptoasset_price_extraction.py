


import pandas as pd
import requests as re

from src.API_Crypto import API_CRYPTO_Nomics



######## Define the Paramter of API ########



HEADER = {'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"}
time_sleep = 1


API_KEY = "d8bd9f65d2056ef411a62282b83778ff"



######## Initialize the API Accesses ########

scraper = API_CRYPTO_Nomics(HEADER,API_KEY)




######## Get All Asset Pairs ########


asset_list = scraper.get_all_asset_pair(exchange="binance")





######## Get Historical Prices of All Crypto Asset ########

start = "2015-01-01T00%3A00%3A00Z"
end = "2020-12-01T00%3A00%3A00Z"




asset_price_df_list = []
error_asset_list = []


for asset in asset_list:
    
    try:
        
        exchange_rate_df = scraper.get_historical_exchange_rate(asset,start,end)

        asset_price_df_list.append(exchange_rate_df)
    
    except:
        
        error_asset_list.append(asset)
        
        time.sleep(time_sleep)



price_df = pd.concat(asset_price_df_list,axis=1)

price_df = price_df.sort_index()
















