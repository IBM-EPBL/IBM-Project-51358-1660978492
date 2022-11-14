#!/usr/bin/env python
# coding: utf-8

# # Water quality Index Calculation

# In[1]:


#Team Lead 1.BharatKumar 2.Ashok 3.Nagababu 4.Kishore
import numpy as np
import pandas as pd


# In[2]:



data = pd.read_csv('water_data.csv', header= 0, encoding= 'unicode_escape') 


# In[3]:


data.head()


# # Exploratory Data Analysis

# In[4]:


data.info()


# In[5]:


data.describe()


# In[6]:


data.isnull().any()


# In[7]:


data.isnull().sum()


# In[8]:


data.dtypes


# In[9]:


data['Temp']=pd.to_numeric(data['Temp'],errors='coerce')
data['D.O. (mg/l)']=pd.to_numeric(data['D.O. (mg/l)'],errors='coerce')
data['PH']=pd.to_numeric(data['PH'],errors='coerce')
data['B.O.D. (mg/l)']=pd.to_numeric(data['B.O.D. (mg/l)'],errors='coerce')
data['CONDUCTIVITY (µmhos/cm)']=pd.to_numeric(data['CONDUCTIVITY (µmhos/cm)'],errors='coerce')
data['NITRATENAN N+ NITRITENANN (mg/l)']=pd.to_numeric(data['NITRATENAN N+ NITRITENANN (mg/l)'],errors='coerce')
data['TOTAL COLIFORM (MPN/100ml)Mean']=pd.to_numeric(data['TOTAL COLIFORM (MPN/100ml)Mean'],errors='coerce')
data.dtypes


# In[10]:


#initialization
start=2
end=1779
station=data.iloc [start:end ,0]
location=data.iloc [start:end ,1]
state=data.iloc [start:end ,2]
do= data.iloc [start:end ,4].astype(np.float64)
value=0
ph = data.iloc[ start:end,5]  
co = data.iloc [start:end ,6].astype(np.float64)   
  
year=data.iloc[start:end,11]
tc=data.iloc [2:end ,10].astype(np.float64)


bod = data.iloc [start:end ,7].astype(np.float64)
na= data.iloc [start:end ,8].astype(np.float64)
na.dtype
data=pd.concat([station,location,state,do,ph,co,bod,na,tc,year],axis=1)
data. columns = ['station','location','state','do','ph','co','bod','na','tc','year']


# In[11]:


data.head()


# # Water Quality index Calculation

# In[12]:


#calulation of Ph
data['npH']=data.ph.apply(lambda x: (100 if (8.5>=x>=7) else(80 if  (8.6>=x>=8.5) or (6.9>=x>=6.8) else(60 if (8.8>=x>=8.6) or (6.8>=x>=6.7) else(40 if (9>=x>=8.8) or (6.7>=x>=6.5)else 0)))))


# In[13]:


#calculation of dissolved oxygen
data['ndo']=data.do.apply(lambda x:(100 if (x>=6) else(80 if  (6>=x>=5.1) else(60 if (5>=x>=4.1) else(40 if (4>=x>=3) else 0)))))


# In[14]:


#calculation of total coliform
data['nco']=data.tc.apply(lambda x:(100 if (5>=x>=0)  else(80 if  (50>=x>=5) else(60 if (500>=x>=50) else(40 if (10000>=x>=500) else 0)))))


# In[15]:


#calc of B.D.O
data['nbdo']=data.bod.apply(lambda x:(100 if (3>=x>=0)  else(80 if  (6>=x>=3) else(60 if (80>=x>=6) else(40 if (125>=x>=80) else 0)))))


# In[16]:


#Calulation of nitrate
data['nna']=data.na.apply(lambda x:(100 if (20>=x>=0) else(80 if  (50>=x>=20) else(60 if (100>=x>=50) else(40 if (200>=x>=100) else 0)))))


# In[17]:


#calculation of electrical conductivity
data['nec']=data.co.apply(lambda x:(100 if (75>=x>=0)  else(80 if  (150>=x>=75) else(60 if (225>=x>=150) else(40 if (300>=x>=225)  else 0)))))


# In[18]:


data['wph']=data.npH * 0.165
data['wdo']=data.ndo * 0.281
data['wbdo']=data.nbdo * 0.234
data['wec']=data.nec* 0.009
data['wna']=data.nna * 0.028
data['wco']=data.nco * 0.281
data['wqi']=data.wph+data.wdo+data.wbdo+data.wec+data.wna+data.wco 


# In[19]:


overall_wqi=data.groupby('year')['wqi'].mean()


# In[20]:


overall_wqi.head()


# In[21]:


data=overall_wqi.reset_index(level=0,inplace=False)
data


# In[22]:


#visualizing the filttered data
year=data['year'].values
AQI=data['wqi'].values
data['wqi']=pd.to_numeric(data['wqi'],errors='coerce')
data['year']=pd.to_numeric(data['year'],errors='coerce')


# In[23]:


import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (20.0, 10.0)
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(year,AQI, color='green')
plt.show()


# In[24]:


data = data[np.isfinite(data['wqi'])]
data.head()


# In[25]:


#scatter plot of data points
cols =['year']
x=data[cols]
y = data['wqi']
plt.scatter(x,y)
plt.show()


# In[26]:


import matplotlib.pyplot as plt
data=data.set_index('year')
data.plot(figsize=(15,6),color="red")
plt.show()


# In[ ]:




