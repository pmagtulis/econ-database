#!/usr/bin/env python
# coding: utf-8

# # Philippine Economy Database

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


gid = "577623777" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df2 = pd.read_csv(url)
df2.head()


# In[6]:


df2.columns = df2.columns.str.replace(' ', "_", regex=False)


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


gid = "127403623" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df3 = pd.read_csv(url)


# In[11]:


gid = "1024176394" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df4 = pd.read_csv(url)


# In[12]:


debt = df3.merge(df4, on='Year')
debt.head()


# ## Fifth sheet

# In[13]:


gid = "1745782387" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df5 = pd.read_csv(url)


# ## Sixth sheet

# In[14]:


gid = "1291603440" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df6 = pd.read_csv(url)


# In[15]:


gid = "1177184243" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df7 = pd.read_csv(url)


# ## Seventh sheet

# In[3]:


gid = "277084577" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df8 = pd.read_csv(url)


# ## Eighth sheet

# In[39]:


gid = "295325838" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df9 = pd.read_csv(url)


# In[48]:


df9.Period = pd.to_datetime(df9.Period, format='%m-%Y')


# ## Ninth sheet

# In[10]:


gid = "1107002312" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df10 = pd.read_csv(url)

df10 = df10.drop(df10.index[17:38])


# ## Tenth sheet

# In[14]:


gid = "2022447349" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df11 = pd.read_csv(url)


# In[20]:


long_ofw = pd.melt(df11, id_vars=['Year'])
long_ofw = long_ofw.drop(long_ofw.index[105:175])
long_ofw.columns = ['Year', 'Deployment type', 'OFWs']


# ## Charts
# 
# ## GDP growth

# In[19]:


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

# In[20]:


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

# In[21]:


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

# In[22]:


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

# In[4]:


spending = alt.Chart(df8).mark_bar().encode(
    x='Year:O',
    y='All expenditures:Q',
    tooltip='All expenditures:Q',
    # The highlight will be set on the result of a conditional statement
    color=alt.condition(
        alt.datum.Year == 2021,  # If the year is 2021 this test returns True,
        alt.value('darkblue'),     # which sets the bar orange.
        alt.value('grey')   # And if it's not true it sets the bar steelblue.
    )
).properties(width=700)

spending


# ## Debt

# In[24]:


debts = alt.Chart(debt).transform_fold(
    ['Debt']
).mark_area(color='darkgreen').encode(
    x='Year:O',
    y='value:Q', 
    tooltip='value:Q'
).properties(width=700)

debts


# ## Tourism

# In[29]:


tourism = alt.Chart(df6).mark_bar().encode(
    x='Year:O',
    y="Foreign arrivals (in million):Q",
    tooltip='Foreign arrivals (in million):Q',
    # The highlight will be set on the result of a conditional statement
    color=alt.condition(
        alt.datum.Year == 2021,  # If the year is 2021 this test returns True,
        alt.value('maroon'),     # which sets the bar orange.
        alt.value('grey')   # And if it's not true it sets the bar steelblue.
    )
).properties(width=700)

tourism


# ## Employment

# In[47]:


employment = alt.Chart(df9).transform_fold(
    ['Unemployment rate']
).mark_line(color='darkgreen').encode(
    x='Period:T',
    y='Unemployment rate:Q', 
    tooltip='value:Q'
).properties(width=700)


employment


# ## OFW deployment

# In[27]:


ofw = alt.Chart(long_ofw).mark_bar().encode(
    x='Year:N',
    y='OFWs',
    color='Deployment type'
).properties(width=700)

ofw


# ## Save the CSVs

# In[27]:


revenue.to_csv('csv/revenue.csv', index=False)
df2.to_csv('csv/pctofGDP.csv', index=False)
growth.to_csv('csv/GDP_growth.csv', index=False)
debt.to_csv('csv/debt.csv', index=False)
df5.to_csv('csv/maturities.csv', index=False)
df6.to_csv('csv/arrivals.csv', index=False)
df7.to_csv('csv/tourism_receipts.csv', index=False)
df8.to_csv('csv/spending.csv', index=False)
df9.to_csv('csv/employment.csv', index=False)
df10.to_csv('csv/annual_employment.csv', index=False)
df11.to_csv('csv/ofw_deployment.csv', index=False)


# ## Save the charts

# In[28]:


revenue_growth.save('charts/revenue_growth.png', scale_factor=2)
deficit.save('charts/deficit.png', scale_factor=2)
econ_growth.save('charts/growth.png', scale_factor=2)
spending.save('charts/expenditures.png', scale_factor=2)
tax.save('charts/tax_effort.png', scale_factor=2)
debts.save('charts/debt.png', scale_factor=2)
tourism.save('charts/arrivals.png', scale_factor=2)
employment.save('charts/unemployment.png', scale_factor=2)
ofw.save('charts/ofw_deployment.png', scale_factor=2)

