import ee
import streamlit as st
import geemap.foliumap as geemap
import datetime
import json
import os

# Hide GitHub icon
st.markdown("""
<style>
#GithubIcon {
  visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# Write service account credentials
with open("service_account.json", "w") as f:
    json.dump(dict(st.secrets["ee_service"]), f)

# Authenticate and initialize Earth Engine
credentials = ee.ServiceAccountCredentials(
    st.secrets["ee_service"]["client_email"],
    "service_account.json"
)
ee.Initialize(credentials)

# App title and instructions
st.title('Raster Calcs')
st.write('Draw a polygon on the map to calculate indices such as NDVI and NDMI.')

# ------------------------ Functions ------------------------

def getNDVI(d1, d2, roi):
    collection = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterDate(d1.strftime('%Y-%m-%d'), d2.strftime('%Y-%m-%d'))
        .select(['B8', 'B4'])
        .filterBounds(roi))
    image = collection.median()
    return image.normalizedDifference(['B8', 'B4']).rename('NDVI')

def getNDMI(d1, d2, roi):
    collection = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterDate(d1.strftime('%Y-%m-%d'), d2.strftime('%Y-%m-%d'))
        .select(['B8', 'B11'])
        .filterBounds(roi))
    image = collection.median()
    return image.normalizedDifference(['B8', 'B11']).rename('NDMI')

# ------------------------ Map Setup ------------------------

m = geemap.Map(center=[20, 78], zoom=4)
m.add_basemap('SATELLITE')
m.add_draw_control()

# Display the map
m.to_streamlit(height=600)

# ------------------------ UI and Processing ------------------------

if m.user_roi:
    try:
        roi = m.user_roi  # This is already an ee.Geometry object

        d1 = st.date_input('Start Date', format='YYYY/MM/DD')
        d2 = st.date_input('End Date', format='YYYY/MM/DD')

        if d1 and d2:
            option = st.selectbox('Calculate', ('NDVI', 'NDMI'), index=None, placeholder='Select Index...')

            if option:
                palette = [
                    'FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718', '74A901',
                    '66A000', '529400', '3E8601', '207401', '056201', '004C00', '023B01',
                    '012E01', '011D01', '011301'
                ]

                if option == 'NDVI':
                    layer = getNDVI(d1, d2, roi)
                    m.addLayer(layer, {'min': -1, 'max': 1, 'palette': palette}, 'NDVI')
                    m.add_legend(title='NDVI', palette=palette, labels=[
                        '-1.0', '-0.8', '-0.6', '-0.4', '-0.2',
                        '0.0', '0.2', '0.4', '0.6', '0.8', '1.0'
                    ])

                elif option == 'NDMI':
                    layer = getNDMI(d1, d2, roi)
                    m.addLayer(layer, {'min': -1, 'max': 1, 'palette': palette}, 'NDMI')
                    m.add_legend(title='NDMI', palette=palette, labels=[
                        '-1.0', '-0.8', '-0.6', '-0.4', '-0.2',
                        '0.0', '0.2', '0.4', '0.6', '0.8', '1.0'
                    ])

                m.to_streamlit(height=600)

    except Exception as e:
        st.error(f"Failed to process drawn region: {e}")
else:
    st.info("Draw a polygon on the map to begin.")
