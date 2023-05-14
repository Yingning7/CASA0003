import streamlit as st

st.set_page_config(
    page_title='CASA0003 Visualisation - Tab 3',
    layout='wide',
    initial_sidebar_state= 'expanded',
    menu_items={
        'Get help': None,
        'Report a Bug': None,
        'About': None
    }
)

st.title('This is Tab 3')

with open('./pages/Workplaces.html', mode='r') as fp:
    html_str = fp.read()

st.components.v1.html(html_str, width=500, height=500)
