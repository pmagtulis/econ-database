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


# ## Percentage of GDP

# In[5]:


gid = "577623777" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df2 = pd.read_csv(url)
df2.head()


# In[6]:


df2.columns = df2.columns.str.replace(' ', '_', regex=False)
df2 = df2.drop(['Budget_balance', 'GDP_growth', 'Expenditures'], axis=1)
df2.head()


# In[7]:


df2.Revenue = df2.Revenue.astype(float)
df2.Tax = df2.Tax.astype(float)


# ## GDP

# In[8]:


gid = "136458205" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
growth = pd.read_csv(url)
growth.head()


# In[9]:


gid = "39713723" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
qgrowth = pd.read_csv(url)
qgrowth.head()


# In[10]:


qgrowth['Quarter'] = pd.to_datetime(
    qgrowth['Quarter'].str.replace(r'(Q\d) (\d+)', r'\2-\1'), errors='coerce')

qgrowth


# In[11]:


gid = "1939522525" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
size = pd.read_csv(url)
size.head()


# ## Debt

# In[12]:


gid = "127403623" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df3 = pd.read_csv(url)
df3.head()


# In[13]:


gid = "1024176394" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df4 = pd.read_csv(url)


# In[14]:


debt = df3.merge(df4, on='Year')
debt.head()


# In[15]:


gid = "1745782387" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df5 = pd.read_csv(url)
df5.head()


# ## Tourism

# In[16]:


gid = "1291603440" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df6 = pd.read_csv(url)


# In[17]:


gid = "1177184243" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df7 = pd.read_csv(url)


# ## Spending

# In[18]:


gid = "277084577" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df8 = pd.read_csv(url)


# ## Labor

# In[19]:


gid = "295325838" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df9 = pd.read_csv(url)


# In[20]:


df9.Period = pd.to_datetime(df9.Period, format='%m-%Y')


# In[21]:


gid = "1107002312" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df10 = pd.read_csv(url)

df10 = df10.drop(df10.index[17:38])


# ## OFWs

# In[22]:


gid = "2022447349" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df11 = pd.read_csv(url)


# In[23]:


long_ofw = pd.melt(df11, id_vars=['Year'])
long_ofw = long_ofw.drop(long_ofw.index[105:175])
long_ofw.columns = ['Year', 'Deployment type', 'OFWs']


# ## Debt interest

# In[24]:


gid = "1933014928" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df12 = pd.read_csv(url)
df12.head()


# ## Inflation

# In[25]:


gid = "1597295529" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df13 = pd.read_csv(url)
df13.head()


# In[26]:


df13.Month = pd.to_datetime(df13.Month, format='%b-%Y')


# ## FDI

# In[27]:


gid = "2137835217" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df14 = pd.read_csv(url)
df14.head()


# ## Twin deficits

# In[51]:


gid = "550743021" #sheet location

url = f"https://docs.google.com/spreadsheets/d/e/{key}/pub?output=csv&gid={gid}"
df15 = pd.read_csv(url)


# In[52]:


df15 = df15.drop(['Reserves import cover (years)'], axis=1)
df15.head()


# ## Charts
# 
# ## GDP growth

# In[30]:


econ_growth = alt.Chart(growth).mark_bar().encode(
    x='Year:O',
    y="Real GDP change:Q",
    tooltip='Real GDP change:Q',
    # The highlight will be set on the result of a conditional statement
    color=alt.condition(
        alt.datum.Year == 2020,  # If the year is 2020 this test returns True,
        alt.value('maroon'),     # which sets the bar orange.
        alt.value('steelblue')   # And if it's not true it sets the bar steelblue.
    )
).properties(width=700)

econ_growth


# ## Revenue growth

# In[31]:


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

# In[32]:


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

# In[33]:


# deficit = alt.Chart(df2).mark_bar().encode(
#     x='Year:O',
#     y="Budget_balance:Q",
#     tooltip='Budget_balance:Q',
#     # The highlight will be set on the result of a conditional statement
#     color=alt.condition(
#         alt.datum.Year == 2021,  # If the year is 2020 this test returns True,
#         alt.value('maroon'),     # which sets the bar orange.
#         alt.value('grey')   # And if it's not true it sets the bar steelblue.
#     )
# ).properties(width=700)

# deficit


# ## Expenditures

# In[34]:


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


# ## Inflation

# In[35]:


inflation = alt.Chart(df13).transform_fold(
    ['Inflation']
).mark_line(color='red').encode(
    x='Month:T',
    y='Inflation:Q', 
    tooltip='value:Q'
).properties(width=700)


inflation


# ## Debt

# In[36]:


debts = alt.Chart(debt).transform_fold(
    ['Debt (in trillion pesos)']
).mark_area(color='darkgreen').encode(
    x='Year:O',
    y='Debt (in trillion pesos):Q', 
    tooltip='value:Q'
).properties(width=700)

debts


# ## Tourism

# In[37]:


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

# In[38]:


employment = alt.Chart(df9).transform_fold(
    ['Unemployment rate']
).mark_line(color='darkgreen').encode(
    x='Period:T',
    y='Unemployment rate:Q', 
    tooltip='value:Q'
).properties(width=700)


employment


# ## OFW deployment

# In[39]:


ofw = alt.Chart(long_ofw).mark_bar().encode(
    x='Year:N',
    y='OFWs',
    color='Deployment type'
).properties(width=700)

ofw


# ## FDI

# In[40]:


fdi = alt.Chart(df14).mark_bar().encode(
    x='Year:O',
    y='FDI net inflows (in billion pesos):Q',
    tooltip='FDI net inflows (in billion pesos):Q',
    # The highlight will be set on the result of a conditional statement
    color=alt.condition(
        alt.datum.Year == 2021,  # If the year is 2021 this test returns True,
        alt.value('red'),     # which sets the bar orange.
        alt.value('grey')   # And if it's not true it sets the bar steelblue.
    )
).properties(width=700)

fdi


# ## Twin deficits

# In[49]:


twin_deficits = alt.Chart(df15).transform_fold(
    ['Budget balance (% of GDP)', 'Current account (% of GDP)']
).mark_line().encode(
    x='Year:O',
    y='value:Q', 
    tooltip='value:Q',
    color='key:N'
).properties(width=700)

twin_deficits


# ## Save the CSVs

# In[42]:


revenue.to_csv('csv/revenue.csv', index=False)
df2.to_csv('csv/pctofGDP.csv', index=False)
growth.to_csv('csv/GDP_growth.csv', index=False)
qgrowth.to_csv('csv/quarterly_growth.csv', index=False)
size.to_csv('csv/size.csv', index=False)
debt.to_csv('csv/debt.csv', index=False)
df5.to_csv('csv/maturities.csv', index=False)
df6.to_csv('csv/arrivals.csv', index=False)
df7.to_csv('csv/tourism_receipts.csv', index=False)
df8.to_csv('csv/spending.csv', index=False)
df9.to_csv('csv/employment.csv', index=False)
df10.to_csv('csv/annual_employment.csv', index=False)
df11.to_csv('csv/ofw_deployment.csv', index=False)
df12.to_csv('csv/debt_interest.csv', index=False)
df13.to_csv('csv/inflation.csv', index=False)
df14.to_csv('csv/fdi.csv', index=False)
df15.to_csv('csv/twin_deficits.csv', index=False)


# ## Save the charts

# In[43]:


revenue_growth.save('charts/revenue_growth.png', scale_factor=2)
econ_growth.save('charts/growth.png', scale_factor=2)
spending.save('charts/expenditures.png', scale_factor=2)
tax.save('charts/tax_effort.png', scale_factor=2)
debts.save('charts/debt.png', scale_factor=2)
tourism.save('charts/arrivals.png', scale_factor=2)
employment.save('charts/unemployment.png', scale_factor=2)
ofw.save('charts/ofw_deployment.png', scale_factor=2)
inflation.save('charts/inflation.png', scale_factor=2)
fdi.save('charts/fdi.png', scale_factor=2)
twin_deficits.save('charts/twin_deficits.png', scale_factor=2)

