#!/usr/bin/env python
# coding: utf-8

# # Using Google APIs to get data from google sheets

# In[2]:


import pandas as pd
import numpy as np
import altair as alt
import requests


# ## Read through first CSV

# In[3]:


key = "2PACX-1vQ_MYZAVCYN_sNTC6XVSq7AO2f7s56zDWrdHD9qSnzK9QugOxfJeE-6IuMBio363KhNnKYxEbsRiDSH"
url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv"
revenue = pd.read_csv(url)
revenue


# ## Government revenue

# In[4]:


revenue.columns = revenue.columns.str.lower()


# In[5]:


revenue.customs = revenue.customs.astype(float)
revenue.bir = revenue.bir.astype(float)
revenue.total = revenue.total.astype(float)
revenue.head()


# ### Chart

# In[6]:


revenues = alt.Chart(revenue).transform_fold(
    ['total', 'bir', 'customs']
).mark_line().encode(
    x='year:O',
    y='value:Q', 
    tooltip='value:Q',
    color='key:N'
).properties(width=700)

revenues


# ## % of GDP

# In[8]:


key = "2PACX-1vQ_MYZAVCYN_sNTC6XVSq7AO2f7s56zDWrdHD9qSnzK9QugOxfJeE-6IuMBio363KhNnKYxEbsRiDSH"
gid = "577623777" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df2 = pd.read_csv(url)
df2


# In[9]:


df2.columns = df2.columns.str.lower()
df2.columns = df2.columns.str.replace(' ', "_", regex=False)
df2.head()


# In[10]:


df2.revenue = df2.revenue.astype(float)
df2.tax = df2.tax.astype(float)
df2.expenditures = df2.expenditures.astype(float)
df2.gdp_growth = df2.gdp_growth.astype(float)
df.head()


# ### Chart
# 
# ### GDP growth

# In[11]:


growth = alt.Chart(df2).mark_bar().encode(
    x='year:O',
    y="gdp_growth:Q",
    tooltip='gdp_growth:Q',
    # The highlight will be set on the result of a conditional statement
    color=alt.condition(
        alt.datum.year == '2020',  # If the year is 2020 this test returns True,
        alt.value('orange'),     # which sets the bar orange.
        alt.value('steelblue')   # And if it's not true it sets the bar steelblue.
    )
).properties(width=700)

growth


# ### Deficit

# In[12]:


deficit = alt.Chart(df2).mark_bar().encode(
    x='year:O',
    y="deficit:Q",
    tooltip='deficit:Q',
    # The highlight will be set on the result of a conditional statement
    color=alt.condition(
        alt.datum.year == '2020',  # If the year is 2020 this test returns True,
        alt.value('red'),     # which sets the bar orange.
        alt.value('grey')   # And if it's not true it sets the bar steelblue.
    )
).properties(width=700)

deficit


# ## Save the charts

# In[ ]:


revenues.save('/charts/revenue.png')
deficit.save('/charts/deficit.png')
growth.save('/charts/growth.png')

