import requests
import os
import pandas as pd

################# Get the items

def get_items_data():
    '''
    This function reads in sales data from a url, writes data to
    a csv file if a local file does not exist, and returns a df.
    '''
    if os.path.isfile('items_df.csv'):
        # Reads the csv saved from above, and assigns to the df variable
        df_items = pd.read_csv('items_df.csv', index_col=0)    
        
    else:
        
        base_url = 'https://python.zach.lol'

        api_url = base_url + '/api/v1/'
        response = requests.get(api_url + 'items')
        data = response.json()
    
        # create list from 1st page
        output = data['payload']['items']

        # loop through the pages and add to list
        while data['payload']['next_page'] != None:
    
            response = requests.get(base_url + data['payload']['next_page'])
            data = response.json()
            output.extend(data['payload']['items'])
    
        df_items = pd.DataFrame(output)

        # Cache data
        df_items.to_csv('items_df.csv')
        
    return df_items

############### get the store data

def get_stores_data():
    '''
    This function reads in stores data from a url, writes data to
    a csv file if a local file does not exist, and returns a df.
    '''
    if os.path.isfile('stores_df.csv'):
        
        # If csv file exists read in data from csv file.
        df_stores = pd.read_csv('stores_df.csv', index_col=0)
        
    else:
        
        base_url = 'https://python.zach.lol'
        api_url = base_url + '/api/v1/stores'
        response = requests.get(api_url)
        data = response.json()
        df_stores = pd.DataFrame(data['payload']['stores'])
        
        # Cache data
        df_stores.to_csv('stores_df.csv')
        
    return df_stores

############# get the sales data

def get_sales_data():
    '''
    This function reads in sales data from a url, writes data to
    a csv file if a local file does not exist, and returns a df.
    '''
    
    if os.path.isfile('sales_df.csv'):
        df_sales = pd.read_csv('sales_df.csv', index_col=0)    
        
    else:
        
        base_url = 'https://python.zach.lol'

        api_url = base_url + '/api/v1/'
        response = requests.get(api_url + 'sales')
        data = response.json()
    
        # create list from 1st page
        output = data['payload']['sales']

        # loop through the pages and add to list
        while data['payload']['next_page'] != None:
    
            response = requests.get(base_url + data['payload']['next_page'])
            data = response.json()
            output.extend(data['payload']['sales'])
    
        df_sales = pd.DataFrame(output)

        # Cache data
        df_sales.to_csv('sales_df.csv')
        
    return df_sales

##################### join the sales, stores and items

def get_joined():
    '''
    This function joins the sales, stores and items dataframes into one
    single data frame and return that df.
    '''
    if os.path.isfile('joined_df.csv'):
        df = pd.read_csv('joined_df.csv', index_col=0) 
    else:
        df_items = get_items_data()
        df_stores = get_stores_data()
        df_sales = get_sales_data()
    
        # left join sales and stores
        df = pd.merge(df_sales, df_stores, left_on='store', right_on='store_id').drop(columns={'store'})
    
        # left join the joined df to the items
        df = pd.merge(df, df_items, left_on='item', right_on='item_id').drop(columns={'item'})

    # Cache data
        df.to_csv('joined_df.csv')
    return df

################ get open power data

def get_open_power_data():
    '''
    This function reads in Open Power Systems Data csv file for Germany, writes data to
    a csv file if a local file does not exist, and returns a df.
    '''
    if os.path.isfile('open_power_df.csv'):
        open_power_df = pd.read_csv('open_power_df.csv', index_col=0)    
        
    else:
        url = 'https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv'
        open_power_df = pd.read_csv(url)
    # Cache data
        open_power_df.to_csv('open_power_df.csv')
    
    return open_power_df
