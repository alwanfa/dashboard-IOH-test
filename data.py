import pandas as pd
import geopandas as gpd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

def choloroplethVisualization(data:pd.DataFrame) :
    try:
        gdf = gpd.read_file("indonesia-gdf-dissolve.geojson")
    except Exception as e:
        st.error(f"An error occurred while loading the GeoJSON file: {e}")
    geodata = gpd.read_file('indonesia-gdf-dissolve.geojson')
    regional_data = data.groupby(["REGION",'region_id']).count().reset_index()
    regional_data['total_project'] = regional_data['NE']
    fig = px.choropleth(regional_data, locations = 'region_id',geojson = geodata, color = 'total_project', color_continuous_scale="peach")
    # fig.show()
    return fig
def implementProjectVisualization(data) :
    years_data = data.groupby('Year').count().reset_index()
    years = years_data["Year"].unique()
    plan = years_data["Plan"]
    actual = years_data["Actual"]
    fig = go.Figure(
        data =[
            go.Bar(name = "Plan", x = years, y = plan),
            go.Bar(name = "Actual", x = years, y = actual)
        ]
    )
    return fig

def getDataByVendor(data) :
    provider_data = data.groupby('Vendor').count().reset_index()
    provider_data['Scope'] = provider_data['NE']
    provider_data['OA %'] = provider_data['Actual']/provider_data['Scope']
    provider_data['OA %'] = provider_data['OA %'].apply(lambda x: f"{(int(x*100))}%")
    provider_data['Unsigned'] = provider_data['Scope']-provider_data["Plan"]
    provider_data = provider_data[['Vendor','Scope','Plan','Actual', 'Unsigned', 'OA %']]
    all = pd.DataFrame(provider_data.sum()).T
    all['Vendor'] = "GRAND TOTAL"
    all['OA %'] = f"{int((all.loc[0,'Actual']/all.loc[0,'Scope'])*100)}%"
    final_df = pd.concat([provider_data, all], ignore_index=True).set_index('Vendor')

    return final_df


def getDeliveryPlanData(data) :
    delivery_plan = data.groupby('Year').count().reset_index()[["Year","Plan", "Actual"]]
    delivery_plan['Year'] = delivery_plan['Year'].apply(lambda x : str(x))
    delivery_plan.set_index('Year', inplace = True)

    return delivery_plan




