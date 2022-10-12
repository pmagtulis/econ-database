#!/usr/bin/env python
# coding: utf-8

# # Using Google APIs to get data from google sheets

# In[47]:


import pandas as pd
import numpy as np
import altair as alt
from googleapiclient.discovery import build
from google.oauth2 import service account


# In[48]:


SERVICE_ACCOUNT_FILE = '/keys.json'

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

creds= None
creds=service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID of spreadsheet.
database= '1ScmJ4rTC9DmHQjOdP-KiAD4cuP2UKfYrbhpdiEot82M' #url of google sheets truncated
service = build('sheets', 'v4')

# Call the Sheets API
sheet = service.spreadsheets()


# ## Government revenue

# In[49]:


revenue = sheet.values().get(spreadsheetId=database,
                            range="Revenue growth!A1:D32").execute()
values = revenue.get('values', [])


# In[50]:


df= pd.DataFrame(values)
df.head()


# In[51]:


df.columns = df.iloc[0]
df = df.drop(0)
df.columns = df.columns.str.lower()


# In[38]:


df.customs = df.customs.astype(float)
df.bir = df.bir.astype(float)
df.total = df.total.astype(float)


# ### Chart

# In[98]:


revenues = alt.Chart(df).transform_fold(
    ['total', 'bir', 'customs']
).mark_line().encode(
    x='year:O',
    y='value:Q', 
    tooltip='value:Q',
    color='key:N'
).properties(width=700)

revenues


# ## % of GDP

# In[83]:


gdp_ratio = sheet.values().get(spreadsheetId=database,
                            range="Revenue % of GDP!A1:H37").execute()
gdp_ratio = gdp_ratio.get('values', [])


# In[84]:


df2= pd.DataFrame(gdp_ratio)
df2.head()


# In[85]:


df2.columns = df2.iloc[0]
df2 = df2.drop(0)
df2.columns = df2.columns.str.lower()
df2.columns = df2.columns.str.replace(' ', "_", regex=False)
df2.head()


# In[86]:


df2.revenue = df2.revenue.astype(float)
df2.tax = df2.tax.astype(float)
df2.expenditures = df2.expenditures.astype(float)
df2.gdp_growth = df2.gdp_growth.astype(float)


# ### Chart
# 
# ### GDP growth

# In[97]:


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

# In[96]:


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


revenue.save('/charts/revenue.png')
deficit.save('/charts/deficit.png')
growth.save('/charts/growth.png')

