import streamlit as st

from io import BytesIO
from PIL import Image

from image import upload_image

st.title("Test")

upload_file = st.file_uploader("Upload Files", type=["jpg", "png"])

if upload_file is not None:
    image = Image.open(upload_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.write("")
    st.write("Predicting...")
    image = Image.open(upload_file)
    image = image.convert("RGB")
    image = image.resize((224, 224))
    upload_image(image)