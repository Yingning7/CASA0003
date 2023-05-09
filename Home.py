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

st.title('CASA0003 Visualisation')
