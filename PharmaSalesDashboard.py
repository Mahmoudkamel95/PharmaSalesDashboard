import numpy as np
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt 
import plotly.express as px 
import streamlit as st
import os
import warnings
warnings.filterwarnings("ignore")
st.set_page_config(page_title="Pharmaceutical Sales Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide",
                   initial_sidebar_state="expanded")

st.title(":bar_chart: Pharma Sales Dashboard")
st.markdown("<style>div.block-container{padding-top:2rem;}</style>",unsafe_allow_html=True)

f1=st.file_uploader(":file_folder: upload a file",type=(["csv","txt","xlsx","xls"]))
if f1 is not None:
    filename= f1.name
    st.write(filename)
    df=pd.read_csv(filename,encoding= "ISO-8859-1")
else:
    
    df =pd.read_csv(r"C:\Users\Swefi Store\Desktop\New folder\pharma-data.csv",encoding= "ISO-8859-1") 

# sidebar
st.sidebar.header("Pharmaceutical Dashboard")
st.sidebar.image(r"C:\Users\Swefi Store\Desktop\New folder\OIP.webp")

st.sidebar.write("")
st.sidebar.write("Filter your data:")
st.sidebar.header("Choose your filter: ")
# create for Region
year=st.sidebar.multiselect("pick your Year", df["Year"].unique())
if not year:
    df2 = df.copy()
else:
    df2 = df[df["Year"].isin(year)]    
  
# Create for State
country= st.sidebar.multiselect("pick the country", df2["Country"].unique())
if not country:
    df3 = df2.copy()
else:
    df3= df2[df2["Country"].isin(country)]

# create for city
city= st.sidebar.multiselect("pick the city",df3["City"].unique())

# filter the data based on Region , State , City

if not year and not country and not city:
    filtered_df = df
elif not country and not city:
    filtered_df = df[df["Year"].isin(year)]
elif not year and not country:
    filtered_df = df[df["Country"].isin(country)]
elif country and city:
    filtered_df = df3[df["Country"].isin(country) & df3["City"].isin(city)  ]      
elif year and city:
    filtered_df = df3[df["Year"].isin(year) & df3["City"].isin(city)]
elif year and country:
    filtered_df = df3[ df3["Year"].isin(year) & df["Country"].isin(country) ]
elif city:
    filtered_df = df3[df3["City"].isin(city)]
else:
    filtered_df = df3[df3["Year"].isin(year) & df3["Country"].isin(country) & df3["City"].isin(city)]

category_df = filtered_df.groupby(by=["Product Class"], as_index = False)["Sales"].sum()
st.sidebar.write("")
st.sidebar.markdown("Made With Dr.Mahmoud Kamel")

 # body
a1, a2, a3, a4 =st.columns(4)
a1.metric("Total Sales", f"{filtered_df['Sales'].sum()/1_000_000_000:.2f} B") 
a2.metric("Total Quantity", f"{filtered_df['Quantity'].sum()/1_000_000:.2f} M") 
a3.metric("Number of Product", filtered_df['Product Name'].nunique())
a4.metric("Number of Customer", filtered_df['Customer Name'].nunique()) 


c1,c2 = st.columns((2))
with c1:
    st.subheader("Sales Per Product Class")
    fig = px.bar(category_df , x = "Product Class", y= "Sales", text = ["${:,.2f}".format(x) for x in category_df["Sales"]],template = "seaborn")
    st.plotly_chart(fig,use_container_width=True, height= 200)

with c2:
    st.subheader("Sales Per Year")
    fig = px.pie(filtered_df,values = "Sales", names= "Year", hole=0.5)
    fig.update_traces(text = filtered_df["Year"], textposition= "outside")
    st.plotly_chart(fig, use_container_width=True)

c1,c2 = st.columns((2))
with c1:
    with st.expander("Product Class_ViewData"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index= False).encode("utf-8")
        st.download_button("Download Data", data= csv , file_name = "Product Class.csv", mime = "text/csv",help = "Click here download the data as a csv file")

with c2:
    with st.expander("Year_ViewData"):
        region= filtered_df.groupby(by= "Year", as_index = False )["Sales"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = category_df.to_csv(index= False).encode("utf-8")
        st.download_button("Download Data", data= csv , file_name = "Year.csv", mime = "text/csv",help = "Click here download the data as a csv file")


st.subheader("Time Series Analysis")


month_order = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]


linechart = (
    filtered_df.groupby("Month")["Sales"].sum().reset_index()
)


linechart["Month"] = pd.Categorical(linechart["Month"], categories=month_order, ordered=True)


linechart = linechart.sort_values("Month")


fig2 = px.line(
    linechart,
    x="Month",
    y="Sales",
    labels={"Sales": "Amount"},
    height=500,
    width=1000,
    template="gridon"
)

st.plotly_chart(fig2, use_container_width=True)

with st.expander("View Data of TimeSeries"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv = linechart.to_csv(index=False).encode("utf-8")
    st.download_button("Download Data", data=csv,file_name= "TimeSeries.csv",mime="text/csv")

# create a treem based on Rear , Channel , Sub_Channel
st.subheader("Hierarchical View of Sales using Treemap")
fig3= px.treemap(filtered_df , path = ["Year","Channel","Sub-channel"], values = "Sales" , hover_data = ["Sales"],color = "Sub-channel")
fig3.update_layout(width = 800 , height = 650)
st.plotly_chart(fig3,use_container_width=True)

cl1,cl2 =st.columns((2))
with cl1:
    st.subheader("Sales Per Sales Team")
    fig = px.pie(filtered_df , values ="Sales", names = "Sales Team", template="plotly_dark")
    fig.update_traces(text = filtered_df["Sales Team"], textposition = "inside")
    st.plotly_chart(fig,use_container_width=True)
with cl2:
    st.subheader("Sales Per Country")
    fig = px.pie(filtered_df , values ="Sales", names = "Country", template="gridon")
    fig.update_traces(text = filtered_df["Country"], textposition = "inside")
    st.plotly_chart(fig,use_container_width=True)



with st.expander("View Data"):
    st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))

# Download original DataSet  
csv = df.to_csv(index = False).encode("utf=8")
st.download_button("Download Data",data = csv , file_name = "Data.csv",mime = "text/csv")

























