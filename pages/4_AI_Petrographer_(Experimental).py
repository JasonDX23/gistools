import streamlit as st
from PIL import Image
import io
# import google.generativeai as genai

# # Set up Gemini API Key
# genai.configure(api_key=st.secrets["API_KEY"])
# model = genai.GenerativeModel(model_name="gemini-1.5-flash")

st.markdown("""
<style>
#GithubIcon {
  visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# Streamlit UI
st.title("The AI Petrographer")
st.subheader('Coming Soon')
st.write("Upload two images of the same thin section: one in Plane Polarized Light and the other in Cross Polarized Light.")

# # Upload images
# col1, col2 = st.columns(2)

# with col1:
#     img1 = st.file_uploader("**Plane Polarized Light (PPL)**", type=["png", "jpg", "jpeg"])

# with col2:
#     img2 = st.file_uploader("**Cross Polarized Light (XPL)**", type=["png", "jpg", "jpeg"])

# # Additional text input
# st.write("#### Optional: Provide Additional Information")
# user_text = st.text_area(
#     "You can add details such as mineral composition, observed structures, or any relevant field notes.", 
#     placeholder="e.g., This sample was collected from a basaltic lava flow in India. It contains plagioclase and clinopyroxene."
# )

# # Function to merge images
# def merge_images(img1, img2):
#     image1 = Image.open(img1).convert("RGB")
#     image2 = Image.open(img2).convert("RGB")

#     # Resize images to the same height
#     height = min(image1.height, image2.height)
#     image1 = image1.resize((int(image1.width * (height / image1.height)), height))
#     image2 = image2.resize((int(image2.width * (height / image2.height)), height))

#     # Combine side-by-side
#     merged_width = image1.width + image2.width
#     merged_image = Image.new("RGB", (merged_width, height))
#     merged_image.paste(image1, (0, 0))
#     merged_image.paste(image2, (image1.width, 0))

#     return merged_image

# # Process button
# if st.button("Analyze Thin Section"):
#     if img1 and img2:
#         # Merge images
#         merged_image = merge_images(img1, img2)

#         # Save to bytes
#         img_bytes = io.BytesIO()
#         merged_image.save(img_bytes, format="PNG")
#         img_bytes.seek(0)

#         # Display the merged image
#         st.image(merged_image, caption="Merged Thin Section Image", use_column_width=True)

#         # Construct the prompt with additional user input
#         prompt = (
#             """"Analyze this petrographic thin section image pair. The left image shows Plane Polarized Light (PPL) and the right shows Cross Polarized Light (XPL) of the same section.

#             Key identification points to consider:
#             - In PPL, focus on: relief, color, pleochroism, cleavage patterns
#             - In XPL, examine: interference colors, extinction angles, twinning patterns

#             Please provide a detailed petrographic description using this structure:

#             1. **Minerals Identified**
#             - List each mineral with key optical properties that led to identification
#             - Note diagnostic features observed in both PPL and XPL

#             2. **Grain Characteristics**
#             - Shape: euhedral/subhedral/anhedral
#             - Size range in mm
#             - Distribution pattern: random/aligned/clustered
#             - Grain boundaries: straight/curved/sutured

#             3. **Textures and Microstructures**
#             - Primary textures (e.g., porphyritic, ophitic)
#             - Secondary features (e.g., alteration, deformation)
#             - Any reaction rims or zoning
#             - Relationships between different mineral phases

#             4. **Genetic Implications**
#             - Evidence for crystallization sequence
#             - Indicators of formation conditions
#             - Signs of metamorphism or alteration

#             5. **Modal Analysis**
#             - Estimated percentage of each mineral
#             - Note any systematic variation in distribution

#             Format the response in Markdown. Specify confidence level for mineral identifications."""
#         )
        
#         if user_text:
#             prompt += f"\nAdditional Information from User: {user_text}\n"

#         # Send to Gemini API
#         response = model.generate_content([prompt, merged_image], stream=True)

#         # Display response
#         st.markdown("### AI Analysis")
#         buffer = []
#         for chunk in response:
#             for part in chunk.parts:
#                 buffer.append(part.text)
#         st.markdown("".join(buffer))

#     else:
#         st.error("Please upload both images.")