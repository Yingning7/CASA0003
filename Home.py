import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title='CASA0003 Visualisation - Home',
    layout='wide',
    initial_sidebar_state= 'expanded',
    menu_items={
        'Get help': None,
        'Report a Bug': None,
        'About': None
    }
)

st.snow()

with st.sidebar:
    st.audio('https://upload.wikimedia.org/wikipedia/commons/b/b9/March_of_the_Volunteers_instrumental.ogg')
    st.video('https://www.youtube.com/watch?v=61-pdq8rItE&ab_channel=AKB48')

st.title('CASA0003 Visualisation')

data = pd.DataFrame(
    [
        ['A', 2020, 52.1, 0.4, 5],
        ['B', 2020, 52.2, 0.4, 10],
        ['C', 2020, 52.3, 0.4, 15],
        ['A', 2021, 52.1, 0.4, 50],
        ['B', 2021, 52.2, 0.4, 100],
        ['C', 2021, 52.3, 0.4, 150],
        ['A', 2022, 52.1, 0.4, 30],
        ['B', 2022, 52.2, 0.4, 10],
        ['C', 2022, 52.3, 0.4, 60]
    ],
    columns=['type', 'year', 'lat', 'lon', 'size']
)

left, right = st.columns(2)
with left:
    selected_year = st.select_slider('year', options=('All',) + tuple(np.sort(data['year'].unique())), value=2021)
with right:
    selected_type = st.multiselect('type', ['All'] + np.sort(data['type'].unique()).tolist(), default=['All'])

data_filtered = data.copy()
if selected_year != 'All':
    data_filtered = data_filtered.loc[data['year'] == selected_year]
    st.balloons()
if 'All' not in selected_type:
    data_filtered = data_filtered.loc[data_filtered['type'].isin(selected_type)]
    st.balloons()

with st.expander('Show DataFrame', expanded=False):
    st.dataframe(data_filtered, use_container_width=True)

map_fig = px.scatter_mapbox(
    data_filtered, 
    lat='lat', 
    lon='lon',
    color='type',
    size='size', 
    size_max=data_filtered['size'].max(), 
    mapbox_style='open-street-map'
)
map_fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})

line_fig = px.line(data_filtered, x='year', y='size', color='type')

st.plotly_chart(map_fig, use_container_width=True)
st.plotly_chart(line_fig, use_container_width=True)

st.write(data)
