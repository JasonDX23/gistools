import streamlit as st
from pathlib import Path
from bs4 import BeautifulSoup
import streamlit
import streamlit.components
import streamlit.components.v1
st.markdown("""
<style>
#GithubIcon {
  visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

ga_code = """<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6295389454311117"
     crossorigin="anonymous"></script>"""

streamlit.components.v1.html(ga_code)
# index_path = Path(st.__file__).parent / "static" / 'index.html'
# soup = BeautifulSoup(index_path.read_text(), features='lxml')

# if not soup.find(id='custom-js'):
#     script_tag = soup.new_tag('script', id='custom-js')
#     script_tag.string = ga_code
#     soup.head.append(script_tag)
#     index_path.write_text(str(soup))

markdown = """A Streamlit web-app to pre-process geospatial data on the go
Made by Jason Dsouza"""

st.sidebar.title("About")
st.sidebar.info(markdown)

st.title("GIS Toolkit")
st.markdown("Pre-process your geospatial data on the go without having to load up resource-intensive desktop applications")
st.divider()


left, middle, right = st.columns(3)
if left.button("Shapefile Visualiser", use_container_width=True):
    st.switch_page('pages/1_Shapefile_Visualiser.py')
if middle.button('Raster Calcs', use_container_width=True):
    st.switch_page('pages/8_Raster_Calcs.py')
if right.button('Plot WMS', use_container_width=True):
    st.switch_page('pages/3_Web_Map_Service_Visualizer.py')
