import streamlit as st
from pathlib import Path
from bs4 import BeautifulSoup
import streamlit
import streamlit.components
import streamlit.components.v1 as components
st.markdown("""
<style>
#GithubIcon {
  visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

markdown = """A Streamlit web-app to pre-process geospatial data on the go
Made by Jason Dsouza"""

st.sidebar.title("About")
st.sidebar.info(markdown)

st.title("GIS Toolkit")
st.markdown("Pre-process your geospatial data on the go without loading up resource-intensive desktop applications")
st.divider()


left, middle, right = st.columns(3)
if left.button("Shapefile Visualiser", use_container_width=True):
    st.switch_page('pages/1_Shapefile_Visualiser.py')
if middle.button('Raster Calcs', use_container_width=True):
    st.switch_page('pages/8_Raster_Calcs.py')
if right.button('Plot WMS', use_container_width=True):
    st.switch_page('pages/3_Web_Map_Service_Visualizer.py')
