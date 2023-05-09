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

data = pd.read_csv('https://raw.githubusercontent.com/Yingning7/CASA0003/master/data/uknights_complete.csv')

left, right = st.columns([1, 2])
with left:
    selected_year = st.select_slider('Year', tuple(np.sort(data['year'].unique())))
    selected_type = st.selectbox('Type', np.sort(data['type'].unique()).tolist())

data_filtered = data.copy()
data_filtered = data_filtered.loc[data['year'] == selected_year]
data_filtered = data_filtered.loc[data_filtered['type'] == selected_type]

map_fig = px.scatter_mapbox(
    data_filtered,
    lat='lat',
    lon='lon',
    color='type',
    size='num_employees',
    hover_name='region',
    size_max=(data_filtered['num_employees'].max()) / 1000,
    zoom=4.65,
    height=700,
    center={'lat': 55.58316, 'lon': -3.833221},
    color_discrete_map={
        'Culture & Leisure': 'red',
        'Culture & Leisure (support)': 'green',
        'Health & Personal Social Services': 'blue',
        'Health & Personal Social Services (support)': 'purple'
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
