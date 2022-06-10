import pandas as pd
import numpy as np
from env import get_db_url
import acquire 
from datetime import datetime

def prepare_zillow(df):

    '''
    This function takes a dataframe and applies several parameters to clean the data in useable form including renmaming
    columns, removing outliers, and changing data types. A cleaned dataframe is returned.
    '''

    df = df.dropna()
    df.rename(columns={'transactiondate':'transaction_date', 'bedroomcnt': 'bedrooms', 'taxvaluedollarcnt': 'tax_value', 'logerror':'log_error', 'bathroomcnt': 'bathrooms', 'calculatedfinishedsquarefeet': 'square_feet', 'yearbuilt': 'year_built'}, inplace=True)
    df = df[df.bathrooms >= 1]
    df= df[df.bathrooms <= 5]
    df = df[df.bedrooms >= 2]
    df = df[df.bedrooms <= 5]
    df = df[df.log_error < 0.55]
    df = df[df.log_error > (-0.31)]
    df = df[df.year_built >= 1910]
    df = df[df.square_feet >= 650]
    df = df[df.square_feet <= 5500]
    df = df[df.tax_value > 40000.0]
    df = df[df.tax_value < 3000000.0]
    df['year_built'] = df['year_built'].astype('int')
    df['fips'] = df['fips'].astype('int')
    df['square_feet'] = df['square_feet'].astype('int')
    df['tax_value'] = df['tax_value'].astype('int')
    df['county'] = df['fips'].replace({6037: 'los_angeles', 6059: 'orange', 6111: 'ventura'})
    df['transaction_date'] = pd.to_datetime(df.transaction_date)

    return df

def prepare_locs(df):

    '''
    This function takes a dataframe and manipulates the format of latitude and longitude columns 
    to be in the correct form. The dataframe is returned with said changes.
    '''
    
    long = pd.DataFrame(df['longitude'])
    for c in long:
        long[c] = (long[c] / 1000000)
    lat = pd.DataFrame(df['latitude'])
    for c in lat:
        lat[c] = (lat[c] / 1000000)
    df.drop(columns = ['latitude', 'longitude'], inplace=True)
    df = pd.concat([df, lat, long], axis=1)

    return df