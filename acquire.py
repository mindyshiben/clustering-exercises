import pandas as pd
import numpy as np
from env import get_db_url
import os

def get_zillow_data():

    '''
    This function acquires zillow data by accessing a SQL database and performing a SQL query to acquire
    selected zillow tables and columns and return it to a dataframe. Additionally, data is stored in a .csv 
    making it more efficient for future utilization of the same function.
    '''

    filename = 'zillow.csv'
    
    if os.path.isfile(filename):
        return pd.read_csv(filename)
    
    else:
        sql = """
        SELECT parcelid, logerror, transactiondate, taxvaluedollarcnt, bedroomcnt, bathroomcnt, yearbuilt, fips, calculatedfinishedsquarefeet, latitude, longitude
        FROM properties_2017
        JOIN predictions_2017 USING (parcelid)
        WHERE transactiondate LIKE '2017%%'
		and propertylandusetypeid = 261;

        """

        df = pd.read_sql(sql, get_db_url('zillow'))

        df.to_csv(filename, index=False)

        return df 

def get_iris_data():
    filename = 'iris.csv'
    
    if os.path.isfile(filename):
        return pd.read_csv(filename)
    
    else:
        sql = """
        SELECT *
        FROM measurements
        JOIN species USING (species_id);
        """

        df = pd.read_sql(sql, get_db_url('iris_db'))

        df.to_csv(filename, index=False)

        return df 
