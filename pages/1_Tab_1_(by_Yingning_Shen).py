import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title='CASA0003 Visualisation - Tab 1 (by Yingning Shen)',
    layout='wide',
    initial_sidebar_state= 'expanded',
    menu_items={
        'Get help': None,
        'Report a Bug': None,
        'About': None
    }
)

st.title('UK Night-Time Workforce 2012-2022 (by Yingning Shen)')

data = pd.read_csv('https://raw.githubusercontent.com/Yingning7/CASA0003/master/data/uknights_complete.csv')
region_lat_lon = pd.read_csv('https://raw.githubusercontent.com/Yingning7/CASA0003/master/data/region_lat_lon.csv')

left, right = st.columns([1, 2])
with left:
    selected_year = st.select_slider('Year', tuple(sorted(data['year'].unique().tolist())))
    selected_group = st.selectbox('Grouper', ['All', 'Primary Group', 'Secondary Group'])
    if selected_group == 'Primary Group':
        selected_type = st.selectbox('Primary Type', sorted(data['primary_type'].unique().tolist()))
    elif selected_group == 'Secondary Group':
        selected_type = st.selectbox('Secondary Type', sorted(data['secondary_type'].unique().tolist()))
    elif selected_group == 'All':
        selected_type = 'All'
    locate = st.selectbox('Locate', ['Whole UK'] + sorted(region_lat_lon['region'].unique().tolist()))

map_data = data.copy()
map_data = map_data.loc[data['year'] == selected_year]
if selected_group == 'All':
    map_data = map_data.groupby(['year', 'region'])['num_employees'].sum().reset_index()
elif selected_group == 'Primary Group':
    map_data = map_data.groupby(['year', 'region', 'primary_type'])['num_employees'].sum().reset_index()
    map_data = map_data.loc[map_data['primary_type'] == selected_type]
elif selected_group == 'Secondary Group':
    map_data = map_data = map_data.loc[map_data['secondary_type'] == selected_type]
map_data['colour_type'] = selected_type
map_data_with_lat_lon = pd.merge(map_data, region_lat_lon, on='region')

if locate == 'Whole UK':
    fig_centre = {'lat': 55.58316, 'lon': -3.833221}
    fig_zoom = 4.65
else:
    fig_centre = {
        'lat': region_lat_lon.loc[region_lat_lon['region'] == locate, 'lat'].item(),
        'lon': region_lat_lon.loc[region_lat_lon['region'] == locate, 'lon'].item()
    }
    fig_zoom = 10

map_fig = px.scatter_mapbox(
    map_data_with_lat_lon,
    lat='lat',
    lon='lon',
    color='colour_type',
    size='num_employees',
    hover_name='region',
    size_max=(map_data_with_lat_lon['num_employees'].max()) / 6000,
    zoom=fig_zoom,
    height=700,
    center=fig_centre,
    color_discrete_map={
        'Culture & Leisure (native)': 'red',
        'Culture & Leisure (support)': 'green',
        'Health & Personal Social Services (native)': 'blue',
        'Health & Personal Social Services (support)': 'purple',
        'Culture & Leisure': 'red',
        'Health & Personal Social Services': 'blue',
        'All': 'orange'
    }
)
map_fig.update_layout(
    mapbox_style='dark',
    mapbox_accesstoken='pk.eyJ1IjoiY2NlNzciLCJhIjoiY2xkMWt6amZzMHF6bjNvcGgwbHlvZzl1ZSJ9.UMSqMJzNGQELF2xTwuZLUw',
    margin={'r': 0, 't': 0, 'l': 0, 'b': 0},
    legend={
        'yanchor': 'top',
        'y': 0.99,
        'xanchor': 'left',
        'x': 0.01
    }
)

with right:
    st.plotly_chart(map_fig, use_container_width=True)


def get_city_df(data: pd.DataFrame, region_name: str, isin: list) -> pd.DataFrame:
    city_data = data.copy()
    if region_name != 'All':
        city_data = city_data.loc[city_data['region'].isin(isin)]
    city_data = city_data.groupby('year')['num_employees'].sum().reset_index().sort_values('year').reset_index(drop=True)
    city_data['region'] = region_name
    city_data['num_employees_ratio'] = city_data['num_employees'] / city_data['num_employees'].max()
    city_data['num_employees_rate_of_change'] = (
            city_data['num_employees'] - city_data['num_employees'].shift(1)
    ) / city_data['num_employees'].shift(1) * 100
    return city_data


city_config = {
    'All': [],
    'Greater London': [
        'City of London',
        'Barking and Dagenham',
        'Barnet',
        'Bexley',
        'Brent',
        'Bromley',
        'Camden',
        'Croydon',
        'Ealing',
        'Enfield',
        'Greenwich',
        'Hackney',
        'Hammersmith and Fulham',
        'Haringey',
        'Harrow',
        'Havering',
        'Hillingdon',
        'Hounslow',
        'Islington',
        'Kensington and Chelsea',
        'Kingston upon Thames',
        'Lambeth',
        'Lewisham',
        'Merton',
        'Newham',
        'Redbridge',
        'Richmond upon Thames',
        'Southwark',
        'Sutton',
        'Tower Hamlets',
        'Waltham Forest',
        'Wandsworth',
        'Westminster'
    ],
    'Greater Manchester': [
        'Bolton',
        'Bury',
        'Manchester',
        'Oldham',
        'Rochdale',
        'Salford',
        'Stockport',
        'Tameside',
        'Trafford',
        'Wigan'
    ],
    'Birmingham': ['Birmingham']
}

line_data = pd.concat([get_city_df(data, region_name, isin) for region_name, isin in city_config.items()], ignore_index=True)

st.dataframe(line_data, use_container_width=True)

line_y = st.selectbox(
    'Ways of visualising number of employees',
    ['num_employees_rate_of_change', 'num_employees_ratio', 'num_employees'],
    format_func=lambda x: ' '.join(x.split('_')).capitalize()
)

st.plotly_chart(px.line(line_data, x='year', y=line_y, color='region'), use_container_width=True)
