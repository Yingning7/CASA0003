import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title='CASA0003 Visualisation - Tab 1',
    layout='wide',
    initial_sidebar_state= 'expanded',
    menu_items={
        'Get help': None,
        'Report a Bug': None,
        'About': None
    }
)

st.title('UK Night-Time Workforce 2012-2022')

data = pd.read_csv('https://raw.githubusercontent.com/Yingning7/CASA0003/master/data/uknights_complete.csv')

left, right = st.columns([1, 2])
with left:
    selected_year = st.select_slider('Year', tuple(np.sort(data['year'].unique())))
    selected_group = st.selectbox('Grouper', ['All', 'Primary Group', 'Secondary Group'])
    if selected_group == 'Primary Group':
        selected_type = st.selectbox('Primary Type', sorted(data['primary_type'].unique().tolist()))
    elif selected_group == 'Secondary Group':
        selected_type = st.selectbox('Secondary Type', sorted(data['secondary_type'].unique().tolist()))
    elif selected_group == 'All':
        selected_type = 'All'

map_data = data.copy()
map_data = map_data.loc[data['year'] == selected_year]
if selected_group == 'All':
    map_data = map_data.groupby(['year', 'region', 'lat', 'lon'])['num_employees'].sum().reset_index()
elif selected_group == 'Primary Group':
    map_data = map_data.groupby(['year', 'region', 'lat', 'lon', 'primary_type'])['num_employees'].sum().reset_index()
    map_data = map_data.loc[map_data['primary_type'] == selected_type]
elif selected_group == 'Secondary Group':
    map_data = map_data = map_data.loc[map_data['secondary_type'] == selected_type]
map_data['use_type'] = selected_type

region_lat_lon = data[['region', 'lat', 'lon']].drop_duplicates().copy()
with left:
    locate = st.selectbox('Locate', ['Whole UK'] + sorted(region_lat_lon['region'].unique().tolist()))
if locate == 'Whole UK':
    centre = {'lat': 55.58316, 'lon': -3.833221}
    zoom = 4.65
else:
    centre = {
        'lat': region_lat_lon.loc[region_lat_lon['region'] == locate, 'lat'].item(),
        'lon': region_lat_lon.loc[region_lat_lon['region'] == locate, 'lon'].item()
    }
    zoom = 10

map_fig = px.scatter_mapbox(
    map_data,
    lat='lat',
    lon='lon',
    color='use_type',
    size='num_employees',
    hover_name='region',
    size_max=(map_data['num_employees'].max()) / 6000,
    zoom=zoom,
    height=700,
    center=centre,
    color_discrete_map={
        'Culture & Leisure (native)': 'red',
        'Culture & Leisure (support)': 'green',
        'Health & Personal Social Services (native)': 'blue',
        'Health & Personal Social Services (support)': 'purple',
        'Culture & Leisure': 'red',
        'Health & Personal Social Services': 'blue'
    }
)
map_fig.update_layout(
    mapbox_style='dark',
    mapbox_accesstoken='pk.eyJ1IjoiY2NlNzciLCJhIjoiY2xkMWt6amZzMHF6bjNvcGgwbHlvZzl1ZSJ9.UMSqMJzNGQELF2xTwuZLUw'
)
map_fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
map_fig.update_layout(
    legend={
        'yanchor': 'top',
        'y': 0.99,
        'xanchor': 'left',
        'x': 0.01
    }
)

with right:
    st.plotly_chart(map_fig, use_container_width=True)
