from io import StringIO
import ee
import streamlit as st
import geemap.foliumap as geemap
import datetime
import json

st.markdown("""
<style>
#GithubIcon {
  visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

service_account = st.secrets['SERVICE_ACCOUNT']
private_key = st.secrets['ee_service']

credentials = ee.ServiceAccountCredentials(service_account, private_key)
ee.Initialize(credentials)

st.title('Raster Calculator')
st.write('Calculate indices such as NDVI, NDMI, NDWI and more for your region of interest')

# Function to calculate NDVI
def getNDVI(d1, d2, roi):
    d1_str = d1.strftime('%Y-%m-%d')
    d2_str = d2.strftime('%Y-%m-%d')
    collection = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
    .filterDate(d1_str, d2_str)
    .select(['B8', 'B4'])
    .filterBounds(roi))

    median_image = collection.median()
    NIR = median_image.select('B8')
    red = median_image.select('B4')

    ndvi = NIR.subtract(red).divide(NIR.add(red))
    return ndvi

def getNDMI(d1, d2, roi):
    d1_str = d1.strftime('%Y-%m-%d')
    d2_str = d2.strftime('%Y-%m-%d')
    collection = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
    .filterDate(d1_str, d2_str)
    .select(['B8', 'B11'])
    .filterBounds(roi))

    median_image = collection.median()
    NIR = median_image.select('B8')
    swir1 = median_image.select('B11')

    ndmi = NIR.subtract(swir1).divide(NIR.add(swir1))
    return ndmi



m = geemap.Map(Draw_export=True)
geojson_file = st.file_uploader('Upload the GeoJSON file here', type='.geojson')

if geojson_file:
    geojson_data = json.load(geojson_file)
    try:
        roi = ee.Geometry(geojson_data["features"][0]["geometry"])
        if roi:
            m.centerObject(roi,zoom=8)
            d1 = st.date_input('Starting Date', value=None, format='YYYY/MM/DD')
            d2 = st.date_input('Ending Date', value=None, format='YYYY/MM/DD')
            if d1 and d2:
                option = st.selectbox('Calculate', ('NDVI', 'NDMI', 'NDWI'),
                                    index=None,
                                    placeholder='Select Indice...')
                # For NDVI
                if option == 'NDVI':
                    palette = [
                            'FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718', '74A901',
                            '66A000', '529400', '3E8601', '207401', '056201', '004C00', '023B01',
                            '012E01', '011D01', '011301'
                        ]

                    m.addLayer(getNDVI(d1, d2, roi), {'palette': palette}, "NDVI")

                elif option == 'NDMI':
                    palette = [
                            'FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718', '74A901',
                            '66A000', '529400', '3E8601', '207401', '056201', '004C00', '023B01',
                            '012E01', '011D01', '011301'
                        ]

                    m.addLayer(getNDMI(d1, d2, roi), {'palette': palette}, "NDMI")
            else:
                st.write('Please select date range')
    except Exception as e:
        st.error(f"Failed to load ROI: {e}")

m.to_streamlit(height=600)