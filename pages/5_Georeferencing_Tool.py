import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
import rasterio as r
from rasterio import transform
from rasterio.shutil import copy as rio_copy
from tempfile import NamedTemporaryFile
import leafmap.foliumap as leafmap


st.markdown("""
<style>
#GithubIcon {
  visibility: hidden;
}
</style>
""", unsafe_allow_html=True)
# Title
st.title('Georeferencer Tool')
st.subheader('Coming Soon')
# # Upload section
# uploaded_file = st.file_uploader(label='Upload an image', type=['jpg', 'jpeg', 'png'], accept_multiple_files=False)

# # Initialize session state
# if 'coordinates' not in st.session_state:
#     st.session_state.coordinates = []

# # Initialize georeferenced image path
# georeferenced_image_path = None

# # Function to collect coordinates
# def process_points(value):
#     if value:
#         x, y = value['x'], value['y']
#         lat = st.text_input("Enter Latitude:", key=f"lat_{x}_{y}")
#         lng = st.text_input("Enter Longitude:", key=f"lng_{x}_{y}")
#         if lat and lng:
#             try:
#                 lat = float(lat)
#                 lng = float(lng)
#                 st.session_state.coordinates.append({
#                     'x': x,
#                     'y': y,
#                     'lat': lat,
#                     'lng': lng
#                 })
#                 st.success(f"Point added: Pixel ({x:.2f}, {y:.2f}) → GPS ({lat}, {lng})")
#             except ValueError:
#                 st.error("Latitude and Longitude must be valid numbers.")

# # Georeferencing function
# def georeference(image_path, points):
#     if len(points) < 2:
#         st.error("At least two ground control points (GCPs) are required for georeferencing.")
#         return None

#     gcps = [r.control.GroundControlPoint(p['x'], p['y'], p['lng'], p['lat']) for p in points]

#     with r.open(image_path) as src:
#         transform_matrix = transform.from_gcps(gcps)
#         metadata = src.meta.copy()
#         metadata.update({
#             'driver': 'GTiff',
#             'crs': 'EPSG:4326',
#             'transform': transform_matrix
#         })

#         with NamedTemporaryFile(delete=False, suffix='.tif') as tmp:
#             out_path = tmp.name
#             with r.open(out_path, 'w', **metadata) as dest:
#                 dest.write(src.read())
#             st.success("Georeferencing complete.")
#             return out_path

# # Convert to Cloud-Optimized GeoTIFF
# def convert_to_cog(src_path):
#     with NamedTemporaryFile(suffix=".tif", delete=False) as tmp:
#         cog_path = tmp.name
#     with r.open(src_path) as src:
#         profile = src.profile.copy()
#         profile.update(
#             driver='COG',
#             compress='deflate',
#             tiled=True,
#             blockxsize=512,
#             blockysize=512
#         )
#         rio_copy(src_path, cog_path, driver='COG', copy_src_overviews=True)
#     return cog_path

# # Main logic
# if uploaded_file is not None:
#     with NamedTemporaryFile(delete=False) as tmp:
#         tmp.write(uploaded_file.getvalue())
#         tmp_path = tmp.name

#     # Show image and capture clicks
#     value = streamlit_image_coordinates(tmp_path, key="local4", use_column_width=True)

#     if value:
#         process_points(value)

#     # Button to trigger georeferencing
#     if st.button("📍 Georeference Image"):
#         if len(st.session_state.coordinates) >= 2:
#             georeferenced_image_path = georeference(tmp_path, st.session_state.coordinates)
#             if georeferenced_image_path:
#                 with open(georeferenced_image_path, "rb") as f:
#                     st.download_button(
#                         label="📥 Download Georeferenced Image (GeoTIFF)",
#                         data=f,
#                         file_name="georeferenced_image.tif",
#                         mime="image/tiff"
#                     )
#         else:
#             st.warning("Please provide at least two ground control points.")

# # Visualization
# if georeferenced_image_path:
#     st.subheader("Visualize Georeferenced Image")
#     cog_path = convert_to_cog(georeferenced_image_path)
#     m = leafmap.Map(center=(0, 0), zoom=2)
#     m.add_cog_layer(cog_path, name="Georeferenced Image")
#     m.to_streamlit()
