



import pandas as pd
import requests as re
from bs4 import BeautifulSoup




class API_CRYPTO():
    """
    This class is used to access to API and extract data.
    This should be a parent class. 
    The child class should correspond to specific data sources.

    """
    
    
    
    def __init__(self,HEADER,API_KEY,common_url_part):

        self.HEADER = HEADER
        self.API_KEY = API_KEY
        self.common_url_part = common_url_part

    def __pull_from_API(self,url):

        pass
        
    
    def get_all_asset_pair(self):
        
        pass
    
       
    def get_current_exchange_rate(self,asset):
         
        pass


    def get_historical_exchange_rate(self,asset):

        pass
        








class API_CRYPTO_Nomics(API_CRYPTO):
    """
    This class is used to access to API of Nomics and extract data.
    This should be a child class. 
    """
    
    
    
    def __init__(self,HEADER,API_KEY):


        super().__init__(HEADER,API_KEY,"https://api.nomics.com/")


    def __pull_from_API(self,url):
        """
        This function pulls the result from the url.
        It also checks the status of the result by status code.

        """

        response = re.get(url, self.HEADER, timeout=10)

        if response.status_code != 200:

            print("Error in Scrapping website.")

            return None

        else:

            return response.json()
        
    
    def get_all_asset_pair(self,exchange="binance"):
        """
        This function is used to extract all the asset pairs available from the exchange.


        :param exchange: str

        :return: list(str)
        """


        url = "{}v1/markets?key={}".format(self.common_url_part,self.API_KEY)

        result = self.__pull_from_API(url)

        if result is None:

            return None

        result_df = pd.DataFrame.from_records(result)

        result_df = result_df[result_df["exchange"]==exchange]


        currency_list = list(set(result_df["base"]))

        return currency_list


    
       
    def get_current_exchange_rate(self):
        """
        This function is used to extract all the asset pairs available from the exchange.

        :param asset: str

        :return: pd.DataFrame

        """

        pass



    def get_historical_exchange_rate(self,asset,start,end):
        """
        This function is used to get the daily exchange rate of the asset pair from the start time to end time.

        :param asset: str
        :param start: str, this string should correspond to the datatime format used in Nomics API (RFC3339)
        :param end: str, this string should correspond to the datatime format used in Nomics API (RFC3339)

        :return: pd.DataFrame

        """

        def get_one_month_data(m_start,m_end):

        	url = "{}v1/currencies/sparkline?key={}&ids={}&start={}&end={}".format(self.common_url_part,self.API_KEY,asset,m_start,m_end)

        	result = self.__pull_from_API(url)

        	if len(result) == 0:

        		return None

        	price_series = pd.Series(result[0]["prices"])
        	price_series.index = result[0]["timestamps"]

        	return price_series

        def create_date_range(start,end):

        	start_time = pd.to_datetime(start[0:10])

        	end_time = pd.to_datetime(end[0:10])

        	date_range = pd.date_range(start_time,end_time,freq="M")

        	date_range = [str(date.date())+"T00%3A00%3A00Z"  for date in date_range]

        	date_range_list = []

        	for idx in range(1,len(date_range)):

        		date_range_list.append((date_range[idx],date_range[idx-1]))

        	return date_range_list



        date_range_list = create_date_range(start,end)


        price_series_list = []

        for time_tup in date_range_list:

        	start = time_tup[1]
        	end = time_tup[0]

        	price_series = get_one_month_data(start,end)

        	price_series_list.append(price_series)

        price_series_list = [series for series in price_series_list if series is not None]


        series = pd.concat(price_series_list,axis=0)

        series = series.drop_duplicates()

        price_df = pd.DataFrame(series)

        price_df.columns = [asset]

        price_df[asset] = price_df[asset].astype(float)


        return price_df




    def get_cryptocurrency_meta_data(self,asset_list,meta_list):

    	asset_string = ",".join(asset_list)
    	meta_string = ",".join(meta_list)

    	url = "{}v1/currencies?key={}&ids={}&attributes={}".format(self.common_url_part,self.API_KEY,asset_string,meta_string)










