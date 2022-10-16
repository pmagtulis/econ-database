#!/usr/bin/env python
# coding: utf-8

# # Using Google APIs to get data from google sheets

# In[1]:


import pandas as pd
import numpy as np
import altair as alt
import requests
from altair_saver import save


# ## Read through first CSV

# In[2]:


key = "2PACX-1vQ_MYZAVCYN_sNTC6XVSq7AO2f7s56zDWrdHD9qSnzK9QugOxfJeE-6IuMBio363KhNnKYxEbsRiDSH"
url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv"
revenue = pd.read_csv(url)
revenue.head()


# ## First sheet

# In[3]:


revenue.customs = revenue.Customs.astype(float)
revenue.bir = revenue.BIR.astype(float)
revenue.total = revenue.Total.astype(float)
revenue.head()


# In[4]:


long = pd.melt(revenue, id_vars=['Year'])
long


# ## Second sheet

# In[5]:


key = "2PACX-1vQ_MYZAVCYN_sNTC6XVSq7AO2f7s56zDWrdHD9qSnzK9QugOxfJeE-6IuMBio363KhNnKYxEbsRiDSH"
gid = "577623777" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df2 = pd.read_csv(url)
df2.head()


# In[6]:


df2.columns = df2.columns.str.replace(' ', "_", regex=False)
df2.head()


# In[7]:


df2.Revenue = df2.Revenue.astype(float)
df2.Tax = df2.Tax.astype(float)
df2.Expenditures = df2.Expenditures.astype(float)
df2.GDP_growth = df2.GDP_growth.astype(float)


# ## Separate GDP growth

# In[8]:


growth = df2[['Year', 'GDP_growth']]
growth.head()


# In[9]:


df2 = df2.drop(['GDP_growth'], axis=1)


# ## Third and fourth sheets

# In[10]:


key = "2PACX-1vQ_MYZAVCYN_sNTC6XVSq7AO2f7s56zDWrdHD9qSnzK9QugOxfJeE-6IuMBio363KhNnKYxEbsRiDSH"
gid = "127403623" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df3 = pd.read_csv(url)
df3.head()


# In[11]:


key = "2PACX-1vQ_MYZAVCYN_sNTC6XVSq7AO2f7s56zDWrdHD9qSnzK9QugOxfJeE-6IuMBio363KhNnKYxEbsRiDSH"
gid = "1024176394" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df4 = pd.read_csv(url)
df4.head()


# In[12]:


debt = df3.merge(df4, on='Period')
debt.columns = debt.columns.str.replace(' ', "_", regex=False)
debt.head()


# ## Fifth sheet

# In[22]:


key = "2PACX-1vQ_MYZAVCYN_sNTC6XVSq7AO2f7s56zDWrdHD9qSnzK9QugOxfJeE-6IuMBio363KhNnKYxEbsRiDSH"
gid = "1745782387" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df5 = pd.read_csv(url)
df5.head()


# ## Charts
# 
# ## GDP growth

# In[13]:


econ_growth = alt.Chart(growth).mark_bar().encode(
    x='Year:O',
    y="GDP_growth:Q",
    tooltip='GDP_growth:Q',
    # The highlight will be set on the result of a conditional statement
    color=alt.condition(
        alt.datum.Year == 2020,  # If the year is 2020 this test returns True,
        alt.value('maroon'),     # which sets the bar orange.
        alt.value('steelblue')   # And if it's not true it sets the bar steelblue.
    )
).properties(width=700)

econ_growth


# ## Revenue growth

# In[14]:


revenue_growth = alt.Chart(long).mark_line().encode(
    x="Year:O",
    y='value:Q',
    color="variable:N",
    row="variable:N"
).properties(
    height=100
)

revenue_growth


# ## Tax and revenue

# In[15]:


tax = alt.Chart(df2).transform_fold(
    ['Tax', 'Revenue']
).mark_line().encode(
    x='Year:O',
    y='value:Q', 
    tooltip='value:Q',
    color='key:N'
).properties(width=700)

tax


# ## Budget balance

# In[16]:


deficit = alt.Chart(df2).mark_bar().encode(
    x='Year:O',
    y="Budget_balance:Q",
    tooltip='Budget_balance:Q',
    # The highlight will be set on the result of a conditional statement
    color=alt.condition(
        alt.datum.Year == 2021,  # If the year is 2020 this test returns True,
        alt.value('maroon'),     # which sets the bar orange.
        alt.value('grey')   # And if it's not true it sets the bar steelblue.
    )
).properties(width=700)

deficit


# ## Expenditures

# In[17]:


spending = alt.Chart(df2).mark_bar().encode(
    x='Year:O',
    y='Expenditures:Q',
    tooltip='Expenditures:Q',
    # The highlight will be set on the result of a conditional statement
    color=alt.condition(
        alt.datum.Year == 2021,  # If the year is 2021 this test returns True,
        alt.value('darkblue'),     # which sets the bar orange.
        alt.value('grey')   # And if it's not true it sets the bar steelblue.
    )
).properties(width=700)

spending


# ## Debt

# In[18]:


debts = alt.Chart(debt).transform_fold(
    ['Debt_levels']
).mark_area(color='darkgreen').encode(
    x='Period:O',
    y='value:Q', 
    tooltip='value:Q'
).properties(width=700)

debts


# ## Save the CSVs

# In[19]:


revenue.to_csv('csv/revenue.csv')
df2.to_csv('csv/pctofGDP.csv')
growth.to_csv('csv/GDP_growth.csv')
debt.to_csv('csv/debt.csv')
df5.to_csv('csv/maturities.csv')


# ## Save the charts

# In[20]:


revenue_growth.save('charts/revenue_growth.png', scale_factor=2)
deficit.save('charts/deficit.png', scale_factor=2)
econ_growth.save('charts/growth.png', scale_factor=2)
spending.save('charts/expenditures.png', scale_factor=2)
tax.save('charts/tax_effort.png', scale_factor=2)
debts.save('charts/debt.png', scale_factor=2)

