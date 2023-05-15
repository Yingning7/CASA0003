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

st.title('CASA0003 Visualisation')

st.markdown(
     f"""
     <style>
     .stApp {{
         background-image: url("https://i.pinimg.com/originals/04/4e/68/044e689920b539251bfe223c4a4a3dd1.jpg");
         background-attachment: fixed;
         background-size: cover
     }}
     </style>
     """,
     unsafe_allow_html=True
 )
