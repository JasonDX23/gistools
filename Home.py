import streamlit as st
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
st.markdown("Pre-process your geospatial data on the go without having to load up resource-intensive desktop applications")
