import streamlit as st

st.set_page_config(
    page_title="AirLock",
    page_icon="🗂️",
    layout="wide",
)

st.title("AirLock – Postcode to 1 km Grid Mapper")

st.write("""
AirLock is a local web tool for linking UK postcodes to 1 km NOx grid cells.
This interface will allow you to upload datasets, run the spatial match, and 
download results.
""")

st.info("The application is under development. Core features will be added in the next chapters.")
