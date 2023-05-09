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

st.title('UK Night Time Economy 2012-2022')

data = pd.read_csv('https://raw.githubusercontent.com/Yingning7/CASA0003/master/pages/uknights_complete.csv')

data['type'] = data['type'].astype(str)


left, right = st.columns([1, 2])
with left:
    selected_year = st.select_slider('year', tuple(np.sort(data['year'].unique())), value=2012)
    selected_type = st.multiselect('type', ['All'] + np.sort(data['type'].unique()).tolist(), default=['All'])

data_filtered = data.copy()
if selected_year != 'All':
    data_filtered = data_filtered.loc[data['year'] == selected_year]
if 'All' not in selected_type:
    data_filtered = data_filtered.loc[data_filtered['type'].isin(selected_type)]

map_fig = px.scatter_mapbox(
    data_filtered,
    lat='lat',
    lon='lon',
    color='type',
    size='num_employees',
    hover_name='region',
    size_max=(data_filtered['num_employees'].max())/1000,
    zoom=4.65,
    height=700,
    center={'lat': 55.58316, 'lon': -3.833221},
    color_discrete_map={'2': 'red', '3': 'green', '4': 'blue', '5': 'purple'}
)
map_fig.update_layout(mapbox_style='dark', mapbox_accesstoken='pk.eyJ1IjoiY2NlNzciLCJhIjoiY2xkMWt6amZzMHF6bjNvcGgwbHlvZzl1ZSJ9.UMSqMJzNGQELF2xTwuZLUw')
map_fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})

with right:
    st.plotly_chart(map_fig, use_container_width=True)
