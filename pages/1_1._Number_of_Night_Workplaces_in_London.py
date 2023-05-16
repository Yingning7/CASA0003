import streamlit as st

st.set_page_config(
    page_title='CASA0003 Visualisation - Number of Night Workplaces in London',
    layout='wide',
    initial_sidebar_state= 'expanded',
    menu_items={
        'Get help': None,
        'Report a Bug': None,
        'About': None
    }
)

st.title('Number of Night Workplaces in London')
st.subheader('by Yunyu Chen')

st.components.v1.iframe('https://yingning7.github.io/', height=700, width=1300, scrolling=True)
