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
    locate = st.selectbox('Locate', ['Whole UK'] + sorted(region_lat_lon['region'].unique().tolist()))
    selected_group = st.selectbox('Grouper', ['All', 'Primary Group', 'Secondary Group'])
    if selected_group == 'Primary Group':
        selected_type = st.selectbox('Primary Type', sorted(data['primary_type'].unique().tolist()))
    elif selected_group == 'Secondary Group':
        selected_type = st.selectbox('Secondary Type', sorted(data['secondary_type'].unique().tolist()))
    elif selected_group == 'All':
        selected_type = 'All'

    st.markdown(
        """
        *Grouper:
        
        - **All**: Numbers of all night-time workers in a selected region and year
        - **Primary Group**: Include two generalised industry groupings of night-time cultural and leisure activities 
        and health and personal social services
        - **Secondary Group**: Include four more specific industry groupings of Night-time cultural and leisure activities, 
        Activities which support night-time cultural and leisure activities, 24-hour health and personal social services 
        and activities which support wider social and economic activities
        """
    )

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
    fig_zoom = 4.55
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
    height=600,
    center=fig_centre,
    color_discrete_map={
        'Culture & Leisure (native)': '#DC143C',
        'Culture & Leisure (support)': '#FF7F50',
        'Health & Personal Social Services (native)': '#6495ED',
        'Health & Personal Social Services (support)': '#9370DB',
        'Culture & Leisure': '#DB7093',
        'Health & Personal Social Services': '#6A5ACD',
        'All': '#FFF8DC'
    },
    labels={'colour_type':'Grouping','num_employees':'Number of employees'}
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
    st.caption(
        'Night-time workers are identified through the Labour Force Survey and are people who "usually" work during '
        'the evening and/or during the night (irrespective of whether they also work during the day).\n'
        'Data sources: https://www.ons.gov.uk/businessindustryandtrade/business/activitysizeandlocation/datasets/employeesworkinginnighttimeindustriesuk.'
    )

st.divider()


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
    'Birmingham': ['Birmingham'],
    'Edinburgh': ['City of Edinburgh', 'Waverley'],
    'Glasgow': ['Glasgow City']

}

line_data = pd.concat([get_city_df(data, region_name, isin) for region_name, isin in city_config.items()], ignore_index=True)

line_fig_1 = px.line(line_data,
                     x='year',
                     y='num_employees_rate_of_change',
                     color='region',
                     markers=True,
                     labels={'region':'Region', 'num_employees_rate_of_change':'Changing Rate','year':'Year'})
line_fig_1.update_layout(
    legend={
        'orientation': 'h',
        'yanchor': 'bottom',
        'y': 1.02,
        'xanchor': 'right',
        'x': 1
    }
)
line_fig_2 = px.line(line_data,
                     x='year',
                     y='num_employees_ratio',
                     color='region',
                     markers=True,
                     labels={'region':'Region', 'num_employees_ratio':'Ratio','year':'Year'})
line_fig_2.update_layout(
    legend={
        'orientation': 'h',
        'yanchor': 'bottom',
        'y': 1.02,
        'xanchor': 'right',
        'x': 1
    }
)

bar_data = data.groupby(['year', 'secondary_type'])['num_employees'].sum().reset_index()
all_data = data.groupby('year')['num_employees'].sum().reset_index()
all_data['secondary_type'] = 'Sum of all 4 industry groupings'
bar_data_1 = pd.concat([bar_data,all_data], ignore_index=True)
bar_fig = px.bar(bar_data_1,
                 x='year',
                 y='num_employees',
                 color='secondary_type',
                 labels={'secondary_type':'Industry Groupings','year':'Year','num_employees':'Number of Employees'})
bar_fig.update_layout(
    legend={
        'orientation': 'h',
        'yanchor': 'bottom',
        'y': 1.02,
        'xanchor': 'right',
        'x': 1
    }
)

st.subheader('Total Number of Employees by Different Industry Groupings (2012-2022)')
st.plotly_chart(bar_fig, use_container_width=True)

st.subheader('Changing Rate and Ratio for Number of Employees (2012-2022)')
tab1, tab2 = st.tabs(["Changing Rate", "Ratio"])
with tab1:
    st.plotly_chart(line_fig_1, use_container_width=True)
with tab2:
    st.plotly_chart(line_fig_2, use_container_width=True)
