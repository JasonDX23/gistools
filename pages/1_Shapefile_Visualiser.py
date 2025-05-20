import streamlit as st
import pyogrio
import pandas as pd
import zipfile
import os
from tempfile import TemporaryDirectory
import leafmap.foliumap as leafmap

# Hide GitHub icon (optional cosmetic tweak)
st.markdown("""
<style>
#GithubIcon {
  visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# UI
st.title("Plot GIS Data Online")
st.info('Upload shapefiles as a zip containing all required components (.shp, .shx, .dbf, .prj)')

# File uploader
uploaded_file = st.file_uploader(
    "Upload a single GIS file",
    type=['geojson', 'kml', 'csv', 'zip'],
    accept_multiple_files=False
)

# Basemap selection
layers = leafmap.basemap_xyz_tiles()
basemap_option = st.selectbox(label='Choose a Basemap', options=list(layers.keys()))

# Create the map
m = leafmap.Map(minimap_control=True)

# Add selected basemap
layer_info = layers[basemap_option]
m.add_tile_layer(
    url=layer_info["url"],
    name=basemap_option,
    attribution=layer_info.get("attribution", "")
)

gdf = None
filename = None

# File handling
if uploaded_file:
    with TemporaryDirectory() as tmpdir:
        filename = uploaded_file.name
        ext = filename.split(".")[-1].lower()
        filepath = os.path.join(tmpdir, filename)

        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())

        try:
            if ext == "geojson":
                m.add_geojson(filepath, layer_name=filename)
                gdf = pyogrio.read_dataframe(filepath)

            elif ext == "kml":
                m.add_kml(filepath, layer_name=filename)
                gdf = pyogrio.read_dataframe(filepath)

            elif ext == "csv":
                df = pd.read_csv(filepath)
                if {"latitude", "longitude"}.issubset(df.columns):
                    m.add_points_from_xy(filepath, layer_name=filename)
                    gdf = df  # Not a GeoDataFrame, but we preserve it
                else:
                    st.warning("CSV must contain 'latitude' and 'longitude' columns.")

            elif ext == "zip":
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    zip_ref.extractall(tmpdir)

                required_exts = {'.shp', '.shx', '.dbf', '.prj'}
                found_files = {f[-4:].lower() for f in os.listdir(tmpdir)}

                if required_exts.issubset(found_files):
                    shp_file = [f for f in os.listdir(tmpdir) if f.endswith(".shp")][0]
                    shp_path = os.path.join(tmpdir, shp_file)
                    gdf = pyogrio.read_dataframe(shp_path)
                    m.add_shp(shp_path, layer_name=shp_file)
                else:
                    st.warning("ZIP is missing required shapefile components.")
        except Exception as e:
            st.error(f"Error reading file: {e}")

# Show map only once
m.to_streamlit(height=500)

# Display metadata and offer conversion if valid data is loaded
if gdf is not None and isinstance(gdf, pd.DataFrame):
    st.markdown(f"**Data Preview**")
    st.dataframe(gdf.head())
    if hasattr(gdf, "crs"):
        st.write("CRS:", gdf.crs)
    st.write("Total Features:", len(gdf))
    if hasattr(gdf, "geom_type"):
        st.write("Geometry Types:", gdf.geom_type.unique())

    # File conversion section
    st.divider()
    st.subheader("**Convert Uploaded Data**")
    shapefile = st.checkbox("Convert to ESRI Shapefile (.zip)")
    geojson = st.checkbox("Convert to GeoJSON")
    csv = st.checkbox("Convert to CSV")
    crs_option = st.selectbox("Choose output CRS", ["Default (Keep original)", "EPSG:4326", "EPSG:3857"])
    file_base_name = st.text_input("Enter output file base name", value="converted_data")

    with TemporaryDirectory() as tmpdir:
        gdf_to_use = gdf
        if hasattr(gdf, "to_crs") and crs_option != "Default (Keep original)":
            gdf_to_use = gdf_to_use.to_crs(crs_option)

        # Export to Shapefile
        if shapefile:
            shp_dir = os.path.join(tmpdir, "shapefile_output")
            os.makedirs(shp_dir, exist_ok=True)
            shp_path = os.path.join(shp_dir, f"{file_base_name}.shp")
            gdf_to_use.to_file(shp_path, driver="ESRI Shapefile")

            zip_path = os.path.join(tmpdir, f"{file_base_name}.zip")
            with zipfile.ZipFile(zip_path, "w") as zipf:
                for file in os.listdir(shp_dir):
                    zipf.write(os.path.join(shp_dir, file), arcname=file)

            st.success("Converted to ESRI Shapefile.")
            with open(zip_path, "rb") as f:
                st.download_button("Download Shapefile (.zip)", f, file_name=f"{file_base_name}.zip")

        # Export to GeoJSON
        if geojson:
            geojson_path = os.path.join(tmpdir, f"{file_base_name}.geojson")
            gdf_to_use.to_file(geojson_path, driver="GeoJSON")
            st.success("Converted to GeoJSON.")
            with open(geojson_path, "rb") as f:
                st.download_button("Download GeoJSON", f, file_name=f"{file_base_name}.geojson")

        # Export to CSV
        if csv:
            csv_path = os.path.join(tmpdir, f"{file_base_name}.csv")
            gdf_to_use.drop(columns="geometry", errors="ignore").to_csv(csv_path, index=False)
            st.success("Converted to CSV.")
            with open(csv_path, "rb") as f:
                st.download_button("Download CSV", f, file_name=f"{file_base_name}.csv")
