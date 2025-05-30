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

# with open("service_account.json", "w") as f:
#     json.dump(dict(st.secrets["ee_service"]), f)

# # Initialize with service account
# credentials = ee.ServiceAccountCredentials(
#     st.secrets["ee_service"]["client_email"],
#     "service_account.json"
# )

service_account = 'streamlit-client@ee-jasondsouza237.iam.gserviceaccount.com'
private_key = r'G:\Github\GISTools\ee-jasondsouza237-d7cfa0b896fb.json'
credentials = ee.ServiceAccountCredentials(service_account, private_key)
ee.Initialize(credentials)

st.title('Unsupervised Classification (using KMeans)')
st.write('')

m = geemap.Map()
geojson_file = st.file_uploader('Upload the GeoJSON file here', type='.geojson')

d1 = st.date_input('Starting Date', value=None, format='YYYY/MM/DD')
d2 = st.date_input('Ending Date', value=None, format='YYYY/MM/DD')
sat_list = ['LANDSAT/LC08/C02/T1','LANDSAT/LC08/C02/T2','LANDSAT/LC09/C02/T1',
            'LANDSAT/LC09/C02/T2','LANDSAT/LE07/C02/T1', 'LANDSAT/LE07/C02/T2',
            'COPERNICUS/S2_HARMONIZED']
option = st.selectbox(label='Choose Satellite', options=sat_list, index=None)

if option:
    if geojson_file:
        geojson_data = json.load(geojson_file)
        try:
            roi = ee.Geometry(geojson_data["features"][0]["geometry"])
            if roi:
                m.centerObject(roi,zoom=8)
                if d1 and d2:
                    if option == 'COPERNICUS/S2_HARMONIZED':
                        image = (
                              ee.ImageCollection('COPERNICUS/S2_HARMONIZED')
                              .filterBounds(roi)
                              .filterDate(d1,d2)
                              .sort("CLOUD_COVER")
                              .first()
                          )

                        vis_params = {"min": 0, "max": 3000, "bands": ["B8", "B4", "B3"]}
                        m.centerObject(roi, 8)
                        m.add_layer(image, vis_params, option)

                    elif option == 'LANDSAT/LC08/C02/T1' or 'LANDSAT/LC08/C02/T2' or'LANDSAT/LC09/C02/T1'or 'LANDSAT/LC09/C02/T2' or 'LANDSAT/LE07/C02/T1'or 'LANDSAT/LE07/C02/T2':
                        image = (
                              ee.ImageCollection(option)
                              .filterBounds(roi)
                              .filterDate(d1,d2)
                              .sort("CLOUD_COVER")
                              .first()
                              .select("B[1-7]")
                          )

                        vis_params = {"min": 0, "max": 3000, "bands": ["B5", "B4", "B3"]}
                        m.centerObject(roi, 8)
                        m.add_layer(image, vis_params, option)
        except:
            st.warning('Please choose a satellite')
                    

m.to_streamlit(height=600)