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

st.components.v1.iframe('https://yingning7.github.io/', height=1500, width=1500, scrolling=True)
