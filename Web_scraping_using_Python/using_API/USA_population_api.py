#!/usr/bin/env python3 

# Program : Collecting data through API
# Author : Ramya Pozhath 

"""
This program collects the population data from 2013 through 2019 for all the states 
in the USA from the API https://datausa.io/api/data and saves it into the csv file 
named us_population_data.csv 
"""

import requests
import pandas as pd


baseurl = "https://datausa.io/api/data"

# constructing a parameter dictionary to be passed for the api call
param_dict  ={}
param_dict["drilldowns"] = "State"
param_dict['measures'] = 'Population'


lst = []

# making the api calls for the years 2013 through 2019 and saving as list of lists. Each sub list 
# corresponds to one year's data. Hence the list has 7 sub lists.
for year in range(2019, 2012, -1):
    param_dict['year'] = year
    resp = requests.get(baseurl, params= param_dict)
    word_ds = resp.json()
    sub_lst = []
    for item in word_ds['data']:
        d ={}
        d['STATE'] = item['State']
        year_ = "POP"+item['Year']
        d[year_] = item['Population']
        sub_lst.append(d)
    lst.append(sub_lst)

# constructing a dataframe with just the state names as a column
state_lst = [k['STATE'] for k in lst[0]]
df = pd.DataFrame(data=state_lst, columns=['STATE'])


# constructing dataframes for each year's data and merging all
for sublst in lst:
        df1 = pd.DataFrame(data=sublst)
        df = pd.merge(df, df1, how="inner", on="STATE")

#saving the dataframe to csv file
df.to_csv("us_population_data.csv", index=False)

