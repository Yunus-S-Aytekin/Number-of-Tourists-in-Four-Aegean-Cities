import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from ipywidgets import interact
import ipywidgets as widgets
from mplcursors import cursor

# link: https://biruni.tuik.gov.tr/bolgeselistatistik/anaSayfa.do?dil=eng

df1 = pd.read_csv("table_1.csv",encoding='latin-1')
df2 = pd.read_csv("table_2.csv",encoding='latin-1')
df3 = pd.read_csv("table_3.csv",encoding='latin-1')
df4 = pd.read_csv("table_4.csv",encoding='latin-1')
df1.replace("Ýzmir","İzmir",inplace=True)
df2.replace("Aydýn","Aydın",inplace=True)
df3.replace("Muðla","Muğla",inplace=True)

for df in [df1,df2,df3,df4]:
    name = df["Region Name"][0]
    df.drop(columns=["Region Code","Region Name"],inplace=True)
    df.set_index("Year",inplace=True)
    df.replace("-",0,inplace=True)
    for i in range(len(df.columns)):
        df.iloc[:,i] = np.int64(df.iloc[:,i])
    df["{}".format(name)] = [np.sum(df.loc[x]) for x in df.index]

data_1 = pd.merge(df1["İzmir"],df2["Aydın"],on="Year")
data_2 = pd.merge(data_1,df3["Muğla"],on="Year")
data = pd.merge(data_2,df4["Denizli"],on="Year")
data = data/1000000

def crs1an(sel):
    sel.annotation.set_text('City: {}\nYear: {}\nNumber of Tourists: {:,}'.format(
        data.columns[0],sel.target[0].astype(int), (sel.target[1]*1000000).astype(int)))
    sel.annotation.get_bbox_patch().set(fc="magenta")
def crs2an(sel):
    sel.annotation.set_text('City: {}\nYear: {}\nNumber of Tourists: {:,}'.format(
        data.columns[1],sel.target[0].astype(int), (sel.target[1]*1000000).astype(int)))
    sel.annotation.get_bbox_patch().set(fc="lime")
def crs3an(sel):
    sel.annotation.set_text('City: {}\nYear: {}\nNumber of Tourists: {:,}'.format(
        data.columns[2],sel.target[0].astype(int), (sel.target[1]*1000000).astype(int)))
    sel.annotation.get_bbox_patch().set(fc="aqua")
def crs4an(sel):
    sel.annotation.set_text('City: {}\nYear: {}\nNumber of Tourists: {:,}'.format(
        data.columns[3],sel.target[0].astype(int), (sel.target[1]*1000000).astype(int)))
    sel.annotation.get_bbox_patch().set(fc="blue")


ax = data.plot(color=["magenta","lime","aqua","blue"],figsize=(13,6),marker="o")
ax.grid(alpha=0.5)
ax.set_ylabel("Number of Tourists (x$10^6$)")
ax.set_title("Change in The Number of Tourists Between The Years 1995 and 2022")
plt.axvspan(2019,2021,alpha=0.5,color="lightgray",label="COVID-19 Pandemic",hatch="/") # x,o,ox,OX,|
plt.gca().spines["top"].set_visible(False)
#plt.gca().spines["left"].set_position("center")
plt.gca().spines["right"].set_visible(False)
plt.xlim((1994.5,2022.5))
plt.xticks(data.index,rotation=45) # rotation
plt.ylim((-0.05,np.max(data.values)+0.05))
plt.legend()

np1 = plt.scatter(data.index,data["İzmir"],alpha=0)
np2 = plt.scatter(data.index,data["Aydın"],alpha=0)
np3 = plt.scatter(data.index,data["Muğla"],alpha=0)
np4 = plt.scatter(data.index,data["Denizli"],alpha=0)
crs1 = cursor(np1)
crs2 = cursor(np2)
crs3 = cursor(np3)
crs4 = cursor(np4)
crs1.connect("add", crs1an)
crs2.connect("add", crs2an)
crs3.connect("add", crs3an)
crs4.connect("add", crs4an)
plt.show()