#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pickle
import pandas as pd


# In[2]:


with open('model.bin', 'rb') as f_in:
    dv, lr = pickle.load(f_in)


# In[3]:


categorical = ['PUlocationID', 'DOlocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df


# In[4]:


df = read_data('data/fhv_tripdata_2021-02.parquet')


# In[5]:


dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = lr.predict(X_val)


# In[8]:


y_pred.mean()


# In[9]:


year = 2021
month = 2
df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')


# In[10]:


df.head()


# In[11]:


# write the ride id and the predictions to a dataframe with results
df_result = pd.DataFrame({'ride_id': df.ride_id, 'prediction': y_pred})


# In[12]:


df_result.to_parquet(
    'output_file',
    engine='pyarrow',
    compression=None,
    index=False
)


# In[ ]:




