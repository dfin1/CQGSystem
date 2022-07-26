#!/usr/bin/env python
# coding: utf-8

# In[1]:

#Required for using this script:
#https://github.com/algoprog/Faspect
#Clone this repo and run faspect.py

import json
import pandas as pd
import requests
import random
import csv


# In[2]:


def callFascetGenerationAPI(body):
    response = requests.post("http://127.0.0.1:6000/extract", json = body )

    if response.status_code !=200:
        print("Error status code:" + str(response.status_code))
    
    #print(response)
    #return only the fasctes
    return (response.json()['facets'])


# ## Dataframe loading:

# In[3]:


df = pd.read_csv("../Data/DF_MIMICS.csv")


# ## Fascet Generation:

# In[ ]:


fascets_5 = []
fascets_12 = []
fascets_20 = []

for idx, item in df.iterrows():
    try:
        body = { "query": item['query'], 
                 "documents": json.loads(item['snippet']) }
        response = callFascetGenerationAPI(body)
        
        fascets_5.append(' , '.join(response[0:5]))
        fascets_12.append(' , '.join(response[0:12]))
        fascets_20.append(' , '.join(response))
        
    except:
        print(idx)
        fascets_5.append(" ")
        fascets_12.append(" ")
        fascets_20.append(" ")
        


try:        
    df['fascets_5'] = fascets_5
    df['fascets_12'] = fascets_12
    df['fascets_20'] = fascets_20
except:
    print("Error! Check dataframe size")


# In[ ]:


df.to_csv("DF_MIMICS_ConstructedFascets")

