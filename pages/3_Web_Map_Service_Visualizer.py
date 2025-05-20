import streamlit as st
import leafmap
import leafmap.foliumap as folium
import ast

st.markdown("""
<style>
#GithubIcon {
  visibility: hidden;
}
</style>
""", unsafe_allow_html=True)
st.set_page_config(layout='wide')
st.title("Web Map Service (WMS)")
st.markdown("""Simply enter the URL of the WMS service
in the text box below and press Enter to retrieve the layers.""")
m = folium.Map(minimap_control=True)

@st.cache_data
def get_layers(wms_url):
    options = leafmap.get_wms_layers(wms_url)
    return options

wms_url = st.text_input("Enter a URL:", value='https://environment.data.gov.uk/spatialdata/lidar-composite-digital-terrain-model-dtm-1m/wms?version=1.3.0')

empty = st.empty()
if wms_url:
    options = get_layers(wms_url)
    default = None
layers = empty.multiselect(
    'Select WMS layers to add to the map',
    options, default=default
)

if layers is not None:
    for layer in layers:
        m.add_wms_layer(wms_url, layers=layer, name=layer)

m.to_streamlit()
