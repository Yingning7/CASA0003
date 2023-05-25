import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import time

st.set_page_config(
    page_title='CASA0003 Visualisation - Night Business Clusters in London',
    layout='wide',
    initial_sidebar_state='expanded',
    menu_items={
        'Get help': None,
        'Report a Bug': None,
        'About': None
    }
)

st.title('Night Business Clusters in London')
st.subheader('by Yichen Song')


def minutes_to_time(minutes):
    hours = minutes // 60
    minutes = minutes % 60
    return time(hours, minutes)


def load_data():
    df = pd.read_csv('https://raw.githubusercontent.com/Yingning7/CASA0003/master/data/location_hours.csv')
    df['open'] = df['open'].apply(minutes_to_time)
    df['close'] = df['close'].apply(minutes_to_time)
    return df


df = load_data()

left, right = st.columns([1, 2])
with left:
    categories_mapping = {
        'All': '',
        'Restaurants': 'restaurants',
        'Pubs': 'pubs',
        'Cocktail Bars': 'cocktailbars',
        'Wine Bars': 'wine_bars',
        'Music Venues': 'musicvenues',
        'Dance Clubs': 'danceclubs'
    }
    categories = list(categories_mapping.keys())
    selected_category = st.selectbox('Category', categories, index=0)

    min_time = min(df['open'].min(), df['close'].min())
    max_time = max(df['open'].max(), df['close'].max())
    time_range = st.slider(
        'Time',
        min_value=min_time,
        max_value=max_time,
        value=(min_time, max_time),
    )

    if selected_category == 'All':
        filtered_data = df[
            (df['open'] <= time_range[1]) &
            (df['close'] >= time_range[0])
            ]
    else:
        selected_category_mapped = categories_mapping[selected_category]
        filtered_data = df[
            (df['category'] == selected_category_mapped) &
            (df['open'] <= time_range[1]) &
            (df['close'] >= time_range[0])
            ]

    category_counts = filtered_data['category'].value_counts()

    count_df = pd.DataFrame({
        'Category': category_counts.index,
        'Counts': category_counts.values
    })

    category_mapping = {
        'restaurants': 'Restaurants',
        'pubs': 'Pubs',
        'cocktailbars': 'Cocktail Bars',
        'wine_bars': 'Wine Bars',
        'musicvenues': 'Music Venues',
        'danceclubs': 'Dance Clubs'
    }

    count_df['Category'] = count_df['Category'].replace(category_mapping)

    st.table(count_df)

    st.markdown(
        """
        *Category*:
        - **All**: Numbers of all night-time business in London

        *Time*:
        - **Selected Time Period**: Businesses that were open during the selected time period

        *Table*:
        - The number of different businesses that were open during the selected time period
        """
    )

with right:
    color_map = {
        'restaurants': 'rgb(31, 119, 180)',
        'pubs': 'rgb(255, 127, 14)',
        'cocktailbars': 'rgb(44, 160, 44)',
        'wine_bars': 'rgb(214, 39, 40)',
        'musicvenues': 'rgb(148, 103, 189)',
        'danceclubs': 'rgb(214, 191, 179)'
    }

    color_map_updated = {
        'restaurants': 'Restaurants',
        'pubs': 'Pubs',
        'cocktailbars': 'Cocktail Bars',
        'wine_bars': 'Wine Bars',
        'musicvenues': 'Music Venues',
        'danceclubs': 'Dance Clubs'
    }

    fig = px.scatter_mapbox(
        filtered_data,
        lat="lat",
        lon="lon",
        color="category",
        color_discrete_map=color_map,
        center={'lat': 51.511316, 'lon': -0.118221},
        zoom=11.5,
        height=800,
        hover_data={"name": True},
        hover_name="name",
        labels={'category': 'Category'}
    )
    fig.update_layout(
        mapbox_style="dark",
        mapbox_accesstoken='pk.eyJ1Ijoic3ljMjAxMzEzIiwiYSI6ImNsZGJrcGczYjAxaHQzcG1pZHNjNDY2N3AifQ.Pq0lIWszrNwo_K8ADm8qgw',
        margin={'r': 0, 't': 0, 'l': 0, 'b': 0},
        autosize=True,
        legend={
            'yanchor': 'top',
            'y': 0.99,
            'xanchor': 'left',
            'x': 0.01,
        },
    )

    for trace in fig.data:
        trace.name = color_map_updated.get(trace.name, trace.name)

    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        'Clusters distribution map of night-time businesses in London. \n'
        'Data sources: [Yelp data API](https://www.yelp.com/developers/documentation/v3)'
    )

st.divider()
st.subheader('Some Specific Night Business Clusters')
st.markdown(
    """
    **Soho**:
    - Soho is one of the most vibrant nightlife areas in London, situated in the western part of the city center. 
    It is home to various restaurants, pubs, music venues, and nightclubs. 
    Soho is renowned for its diverse cultural atmosphere and abundant entertainment options.

    **Central London**:
    - Central London serves as a significant hub for night-time businesses. 
    This area boasts numerous upscale restaurants, pubs, and cocktail bars, particularly near renowned shopping districts such as Oxford Street, The City of London, Westminster and Covent Garden.
    Central London is also home to some historic music venues and theaters.

    **East London**:
    - In recent years, East London has emerged as a hotspot for nightlife. 
    Areas such as Shoreditch and Islington feature fashionable bars, cocktail bars, and music venues, attracting young people and creative individuals.

    **Canary Wharf**:
    - As the hub of London's financial district, Canary Wharf is a gathering place for night-time businesses. 
    It offers upscale restaurants and bars suitable for business gatherings and social events.
    """
)

st.divider()
left, right = st.columns([1, 1])
with left:
    data = {
        'Category': ['restaurants', 'pubs', 'cocktailbars', 'winebars', 'musicvenues', 'danceclubs'],
        '2019': [737.1154, 688.3887, 788.6455, 717.2254, 795.1128, 882.8205],
        '2020': [737.7564, 702.1611, 819.5965, 739.422, 833.0075, 1040.2564],
        '2021': [742.8625, 699.4757, 822.536, 725.2457, 850.8271, 1020.2564],
        '2022': [741.9551, 698.133, 812.5072, 730.3613, 798.0451, 985.8974],
        '2023': [712.1795, 693.913, 756.5706, 722.1977, 794.2105, 923.0769]
    }
    df = pd.DataFrame(data)
    df_t = df.melt('Category', var_name='Year', value_name='Time')
    fig = go.Figure()
    for category in df_t['Category'].unique():
        category_df = df_t[df_t['Category'] == category]
        fig.add_trace(go.Scatter(
            x=category_df['Year'],
            y=category_df['Time'],
            name=category.capitalize(),
            mode='lines+markers'
        )
        )
    fig.update_layout(
        title={
            'text': 'Average Opening Time for Night Businesses in London',
            'font': {'size': 26}
        },
        xaxis=dict(title='Year', tickmode='array', tickvals=[2019, 2020, 2021, 2022, 2023],
                   ticktext=['2019', '2020', '2021', '2022', '2023']),
        yaxis=dict(title='Time'),
        legend=dict(orientation='h', yanchor='bottom', y=1, xanchor='right', x=1, title='Category'),
        margin=dict(t=100),
        autosize=True
    )
    y_range = ['11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00']
    y_values = [int(y.split(':')[0]) * 60 + int(y.split(':')[1]) for y in y_range]
    fig.update_yaxes(range=[y_values[0], y_values[-1]], tickmode='array', tickvals=y_values, ticktext=y_range)
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        'Data sources: [Yelp data API](https://www.yelp.com/developers/documentation/v3)'
    )

with right:
    data1 = {
        'Category': ['restaurants', 'pubs', 'cocktailbars', 'winebars', 'musicvenues', 'danceclubs'],
        '2019': [1366.4904, 1439.0217, 1459.8847, 1385.7225, 1473.609, 1599.7436],
        '2020': [1348.7179, 1371.2724, 1413.2853, 1292.7312, 1402.1053, 1451.7949],
        '2021': [1302.0192, 1401.8095, 1357.781, 1368.468, 1384.9624, 1489.4872],
        '2022': [1351.7628, 1401.0246, 1433.3429, 1362.0087, 1387.218, 1523.4615],
        '2023': [1366.6667, 1413.6637, 1461.0086, 1374.4509, 1491.6541, 1594.8718]
    }
    df1 = pd.DataFrame(data1)
    df_t1 = df1.melt('Category', var_name='Year', value_name='Time')
    fig1 = go.Figure()
    for category in df_t1['Category'].unique():
        category_df = df_t1[df_t1['Category'] == category]
        fig1.add_trace(go.Scatter(
            x=category_df['Year'],
            y=category_df['Time'],
            name=category.capitalize(),
            mode='lines+markers'
        )
        )
    fig1.update_layout(
        title={
            'text': 'Average Closing Time for Night Businesses in London',
            'font': {'size': 26}
        },
        xaxis=dict(title='Year', tickmode='array', tickvals=[2019, 2020, 2021, 2022, 2023],
                   ticktext=['2019', '2020', '2021', '2022', '2023']),
        yaxis=dict(title='Time'),
        legend=dict(orientation='h', yanchor='bottom', y=1, xanchor='right', x=1, title='Category'),
        margin=dict(t=100),
        autosize=True
    )
    y_range = ['21:00', '22:00', '23:00', '0:00', '1:00', '2:00', '3:00']
    y_values = [1260, 1320, 1380, 1440, 1500, 1560, 1620]
    fig1.update_yaxes(range=[y_values[0], y_values[-1]], tickmode='array', tickvals=y_values, ticktext=y_range)
    st.plotly_chart(fig1, use_container_width=True)
    st.caption(
        'Data sources: [Yelp data API](https://www.yelp.com/developers/documentation/v3)'
    )
