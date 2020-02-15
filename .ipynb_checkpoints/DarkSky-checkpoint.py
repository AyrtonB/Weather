import pandas as pd
import requests
from datetime import datetime

class Wrapper():
    dt_2_unix = lambda self, datetime: int(datetime.timestamp())
    timestamp_2_unix = lambda self, timestamp: (timestamp - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s') 

    def construct_url(self, latitude, longitude, time=None, query={}):
        ## Preparing parameters
        default_params = {
            'units' : 'si',
            'lang' : 'en',
            'extend' : 'hourly',
        }
        
        default_params.update(query)
        
        ## Constructing main url
        url_root = 'https://api.darksky.net/forecast'
        url = f'{url_root}/{self.API_key}/{latitude},{longitude}'
        
        ## Handling time 
        if time:
            if isinstance(time, datetime):
                time = self.dt_2_unix(time)
                
            if isinstance(time, pd.Timestamp):
                time = self.timestamp_2_unix(time)
            
            url += f',{time}'
                
        ## Adding query parameters
        query_params = '?'

        for query_param, param_value in default_params.items():
            query_params += f'{query_param}={param_value}&'

        query_url = url + query_params[:-1] # We dont want the last '&'

        return query_url
    
    def url_2_df(self, query_url):
        r = requests.get(query_url)
        r_json = r.json()

        df = pd.DataFrame(r_json['hourly']['data'])
        df['time'] = df['time'].apply(datetime.fromtimestamp)

        return df
    
    def lat_lon_dt_2_df(self, latitude, longitude, time=None, query={}):
        query_url = self.construct_url(latitude, longitude, time=time, query=query)
        df = self.url_2_df(query_url)
        
        return df
        
    def __init__(self, API_key):
        self.API_key = API_key
        