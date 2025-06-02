import streamlit as st
import osmnx as ox
import folium
from folium.plugins import Draw
import geopandas as gpd
from streamlit_folium import st_folium
from shapely.geometry import shape
import pandas as pd
import zipfile
import os
from tempfile import TemporaryDirectory

st.markdown("""
<style>
#GithubIcon {
  visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

st.title('GIS Vector Downloader')
st.markdown('Draw a polygon covering the area of interest to download it as an ESRI Shapefile')

m = folium.Map()
Draw(export=False).add_to(m)

output = st_folium(m, width=725, height=500)

if output and 'all_drawings' in output:
    features = output['all_drawings']
    if features:
        geometries = [shape(feature['geometry']) for feature in features]
        gdf = gpd.GeoDataFrame(geometry=geometries, crs='EPSG:4326')
        polygon = gdf.iloc[0]['geometry']

        # 1. Get road network from the polygon
        g = ox.graph_from_polygon(polygon, network_type='all')
        _, edges = ox.graph_to_gdfs(g, edges=True)

        # 2. Get building and other features using geometries_from_polygon
        tags = {
            'building': True,
            'landuse': True
        }
        buildings = ox.features_from_polygon(polygon, tags=tags)
        
        # Keep only relevant columns (geometry and address)
        buildings = buildings.loc[:, buildings.columns.str.contains('addr:|geometry')]
        buildings = buildings[buildings.geometry.type.isin(['Polygon', 'MultiPolygon'])]

        # 3. Ensure matching CRS for all geometries
        edges = edges[['geometry']].to_crs(buildings.crs)
        
        # 4. Combine road and building geometries into one GeoDataFrame
        combined = gpd.GeoDataFrame(pd.concat([edges, buildings], ignore_index=True), crs=edges.crs)

        if not combined.empty:
            with TemporaryDirectory() as tmpdir:
                shp_dir = os.path.join(tmpdir, "shapefile_output")
                os.makedirs(shp_dir, exist_ok=True)
                shp_path = os.path.join(shp_dir, "osm_data.shp")
                
                # Save to shapefile
                combined.to_file(shp_path, driver="ESRI Shapefile")

                # Zip the shapefile
                zip_path = os.path.join(tmpdir, "osm_data.zip")
                with zipfile.ZipFile(zip_path, "w") as zipf:
                    for file in os.listdir(shp_dir):
                        zipf.write(os.path.join(shp_dir, file), arcname=file)

                # Provide download link
                st.success("Converted to ESRI Shapefile.")
                with open(zip_path, "rb") as f:
                    st.download_button("Download Shapefile (.zip)", f, file_name="osm_data.zip")

else:
    st.info('No AOI drawn yet')
