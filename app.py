import pandas as pd
import plotly.express as px
from data import choloroplethVisualization, implementProjectVisualization, getDataByVendor, getDeliveryPlanData
import streamlit as st

st.set_page_config(
    page_title = "Network Project Dashboard",
    page_icon = '📊',
    layout = 'wide'

)
data = pd.read_csv("data/test_case.csv")

# print(data)


# ------ SIDEBAR -----------

st.sidebar.header("Filter here")
ne = st.sidebar.multiselect(
    "Select Network Element",
    options = data['NE'].unique(),
    # default = data['NE'].unique()
)

region = st.sidebar.multiselect(
    "Select Region",
    options = data['REGION'].unique(),
    # default = data['REGION'].unique()
)

year = st.sidebar.multiselect(
    "Select Year",
    options = data['Year'].unique(),
    # default = data['Year'].unique()
)

project = st.sidebar.multiselect(
    "Select Project",
    options = data['PROJECT'].unique(),
    # default = data['PROJECT'].unique()
)


query = " & ".join([
    ("NE == @ne") if ne else "True",
    ("REGION == @region") if region else "True",
    ("Year == @year") if year else "True",
    ("PROJECT == @project") if project else "True"
])

data_selection = (data.query(query)) if query != "True & True & True & True" else data
# print(data_selection)

chloropleth = choloroplethVisualization(data_selection)
chloropleth.update_geos(fitbounds="locations", visible=False)
chloropleth.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'),
                          margin={"r":0,"t":0,"l":0,"b":0})
# st.plotly_chart(chloropleth)

implement_project = implementProjectVisualization(data_selection)

c1 = st.columns(2)
c1[0].subheader('Peta Persebaran Project')
c1[0].plotly_chart(chloropleth)
c1[1].subheader('Perbandingan Plan dan Actual Project (Bar Chart)')
c1[1].plotly_chart(implement_project)

vendor_data = getDataByVendor(data)
delivery_plan_data = getDeliveryPlanData(data)

c2 = st.columns(2)
c1[0].subheader('Data Project Berdasarkan Vendor')
c1[0].dataframe(vendor_data)
c1[1].subheader('Perbandingan Plan dan Actual Project')
c1[1].dataframe(delivery_plan_data)

st.subheader('Dataset Project')
st.dataframe(data_selection)