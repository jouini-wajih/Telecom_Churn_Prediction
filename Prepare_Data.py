import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.core.indexes.period import Index

data = pd.read_csv("dataset_telecom.csv",encoding='latin-1')
def d_clean(data):
 data=data.iloc[:,1:]
 from sklearn.preprocessing import LabelEncoder
 label_encoder = LabelEncoder()
 print(data.shape)
 data['active_msg_vocaux'] = label_encoder.fit_transform(data['active_msg_vocaux'])
 data['churn'] = label_encoder.fit_transform(data['churn'])
 data_clean=data.dropna()

 x=data_clean['duree_appel_jour(minutes)']
 y=data_clean['nb_appel_jour']
 Avg_duree_per_app=(x/y).mean()
 I=data['nb_appel_jour'][data['nb_appel_jour'].isnull()].index
 data['nb_appel_jour'].__setitem__(I,data['duree_appel_jour(minutes)'].__getitem__(I)/Avg_duree_per_app)

 x=data_clean['duree_appel_nuit(minutes)']
 y=data_clean['nb_appel_nuit']
 Avg_duree_per_app_nuit=(x/y).mean()

 I=data['nb_appel_nuit'][data['nb_appel_nuit'].isnull()].index
 data['nb_appel_nuit'].__setitem__(I,data['duree_appel_nuit(minutes)'].__getitem__(I)/Avg_duree_per_app_nuit)

 x=data_clean['duree_appel_soiree(minutes)']
 y=data_clean['nb_appel_soiree']
 Avg_duree_per_app_soiree=(x/y).mean()

 I=data['nb_appel_soiree'][data['nb_appel_soiree'].isnull()].index
 for i in I:
   data['nb_appel_soiree'].iloc[i]=data['duree_appel_soiree(minutes)'].iloc[i]/Avg_duree_per_app_soiree

 avg=data['nb_jours_abonne'].mean()
 I=data[data['nb_jours_abonne'].isnull()].index
 for i in I:
   data['nb_jours_abonne'].iloc[i]=avg

 avg=data['nb_reclamation'].mean()
 I=data[data['nb_reclamation'].isnull()].index
 for i in I:
   data['nb_reclamation'].iloc[i]=avg

 x=data_clean['duree_appel_inter(minutes)'][data_clean['duree_appel_inter(minutes)']!=0]
 y=data_clean['nb_appel_inter'][data_clean['nb_appel_inter']!=0]
 Avg_duree_per_app_inter=(y/x).mean()
 I=data['nb_appel_inter'][data['nb_appel_inter'].isnull()].index
 for i in I:
   data['nb_appel_inter'].iloc[i]=data['duree_appel_inter(minutes)'].iloc[i]*Avg_duree_per_app_inter

 cout_per_min_avg=(data_clean['cout_appel_jour']/data_clean['duree_appel_jour(minutes)']).mean()
 I=data['cout_appel_jour'][data['cout_appel_jour'].isnull()].index
 for i in I:
   data['cout_appel_jour'].iloc[i]=cout_per_min_avg*data['duree_appel_jour(minutes)'].iloc[i]
 return data



data=d_clean(data)

x=data[data['churn']!=2].iloc[:,:-1]
y=data[data['churn']!=2].iloc[:,-1:]
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.1,stratify=y,random_state=1)

from sklearn.ensemble import RandomForestClassifier
rfc=RandomForestClassifier()
rfc.fit(x_train,y_train)
train_pred=rfc.predict(x_train)
z=data[data['churn']==2].iloc[:,:-1]
pred=rfc.predict(z)
pred
I=z.index
data['churn'].iloc[I]=pred

data3=data[data['active_msg_vocaux']!=2]
x=data3.drop(columns=['active_msg_vocaux'])
y=data3["active_msg_vocaux"]
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.1,stratify=y,random_state=1)

lr2=LogisticRegression()
lr2.fit(x_train,y_train)
predy=lr2.predict(x_train)

I = data[data['active_msg_vocaux']==2]
d=(I.drop(columns=['active_msg_vocaux']))
data['active_msg_vocaux'][data['active_msg_vocaux']==2]=lr2.predict(d)


def Df():
  return data
def pred(x):
  return pd.DataFrame(rfc.predict_proba(x.iloc[:,:-1])).iloc[:,1]
data['churn_proba']=pred(data)

Df()