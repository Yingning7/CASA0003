import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title='CASA0003 Visualisation - UK Night-Time Workforce',
    layout='wide',
    initial_sidebar_state= 'expanded',
    menu_items={
        'Get help': None,
        'Report a Bug': None,
        'About': None
    }
)

st.title('UK Night-Time Workforce 2012-2022')
st.subheader('by Yingning Shen')

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
        - **Secondary Group**: Include four more specific industry groupings of night-time cultural and leisure activities, 
        activities which support night-time cultural and leisure activities, 24-hour health and personal social services 
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
    fig_zoom = 9.5

map_fig = px.scatter_mapbox(
    map_data_with_lat_lon,
    lat='lat',
    lon='lon',
    color='colour_type',
    size='num_employees',
    hover_name='region',
    size_max=(map_data_with_lat_lon['num_employees'].max()) / 5000,
    zoom=fig_zoom,
    height=600,
    center=fig_centre,
    color_discrete_map={
        'Culture & Leisure (native)': '#DC143C',
        'Culture & Leisure (support)': '#FF7F50',
        '24-hr Health & Personal Social Services': '#6495ED',
        'Activities Supporting Wider Social & Economics Activities': '#9370DB',
        'Culture & Leisure': '#DB7093',
        'Others': '#6A5ACD',
        'All': '#FFF8DC'
    },
    labels={'colour_type': 'Grouping', 'num_employees': 'Number of employees'}
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

line_fig_1 = px.line(
    line_data,
    x='year',
    y='num_employees_rate_of_change',
    color='region',
    markers=True,
    labels={'region': 'Region', 'num_employees_rate_of_change': 'Changing Rate', 'year': 'Year'},
    color_discrete_sequence=px.colors.qualitative.Safe
)
line_fig_1.update_layout(
    legend={
        'orientation': 'h',
        'yanchor': 'bottom',
        'y': 1.02,
        'xanchor': 'right',
        'x': 1
    }
)

line_fig_2 = px.line(
    line_data,
    x='year',
    y='num_employees_ratio',
    color='region',
    markers=True,
    labels={'region': 'Region', 'num_employees_ratio': 'Ratio', 'year': 'Year'},
    color_discrete_sequence=px.colors.qualitative.Safe
)
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
bar_fig = px.bar(
    bar_data,
    x='year',
    y='num_employees',
    color='secondary_type',
    labels={'secondary_type': 'Industry Groupings', 'year': 'Year', 'num_employees': 'Number of Employees'}
)
bar_fig.update_layout(
    legend={
        'orientation': 'h',
        'yanchor': 'bottom',
        'y': 1.02,
        'xanchor': 'right',
        'x': 1
    }
)

gap_data = data.groupby(['year', 'region'])['num_employees'].sum().reset_index().sort_values(
    ['region', 'year']
).reset_index(drop=True).groupby('region').agg(
    {
        'num_employees': ['first', 'last']
    }
).reset_index().droplevel(0, axis=1).rename(columns={'': 'region'})
gap_data['diff'] = gap_data['last'] - gap_data['first']
gap_data['diff_percentage'] = gap_data['diff'] / gap_data['first'] * 100
gap_data = gap_data.sort_values('diff', ascending=False).reset_index(drop=True)
gap_data_1 = gap_data.sort_values('diff_percentage', ascending=False).reset_index(drop=True)

left, right = st.columns(2)
with left:
    st.subheader('Total Number of Employees by Different Industry Groupings (2012-2022)')
    st.plotly_chart(bar_fig, use_container_width=True)
    st.caption(
        'Activities which support wider social and economic activities has been the largest proportions in ten years'
        ' among all four industry groupings. Number of night-time workers for cultural and leisure activities'
        ' decreased since the COVID-19 pandemic begins.'
    )
with right:
    st.subheader('Top 10 Regions with the Greatest Increase of Night-Time Workers (2012-2022)')
    tab3, tab4 = st.tabs(["By Number", "By Percentage"])
    with tab3:
        st.plotly_chart(px.bar(gap_data.head(10), x='region', y='diff'), use_container_width=True)
    with tab4:
        st.plotly_chart(px.bar(gap_data_1.head(10), x='region', y='diff_percentage'), use_container_width=True)

st.subheader('Changing Rate and Ratio for Number of Employees in Different Regions (2012-2022)')
tab1, tab2 = st.tabs(["Changing Rate", "Ratio"])
with tab1:
    st.plotly_chart(line_fig_1, use_container_width=True)
    st.caption(
        'For the whole UK, the changing rate of night-time workers became smaller after 2017 and had a negative growth'
        ' in the year of 2021, but then had a rapid rebound in 2022. The negative growth in 2021 might be an impact of the pandemic.'
        ' For Greater London area, the changing rate had a negative growth in 2022, this might relate to economic depression'
        ' and inflation happened recently. For Edinburgh, the changing rate has become negative since 2020 and had a recovery in 2022'
        ' although still a negative growth. For other three regions, there is no obvious patterns in changing rate that we'
        ' can observe directly.'
    )

with tab2:
    st.plotly_chart(line_fig_2, use_container_width=True)
    st.caption(
        'For the whole UK, the number of night-time employees grew gradually and reached the maximum in 2022'
        ' but the rate become slower after 2017. Similarly for Greater Manchester area and Birmingham that the'
        ' number of night-time employees reached the maximum in 2022. For Greater London area, the number of'
        ' night-time employees reached the maximum in 2021 and had a decrease in 2022. For Edinburgh, the number of'
        ' night-time employees reached the maximum in 2020. For Glasgow, the number of night-time employees reached'
        ' the maximum in 2017 and then experienced a sharp decline between 2017 and 2018.'
    )
