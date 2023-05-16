import streamlit as st

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

st.title('UK Night-Time Economy')
st.subheader('Data Visualisation by Group 12 for CASA0003')

st.markdown(
     f"""
     <style>
     .stApp {{
         background-image: url("https://raw.githubusercontent.com/Yingning7/CASA0003/master/WechatIMG523.jpeg");
         background-attachment: fixed;
         background-size: cover
     }}
     </style>
     """,
     unsafe_allow_html=True
 )
