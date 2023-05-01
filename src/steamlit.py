import streamlit as st

from io import BytesIO
from PIL import Image

from fastapi import APIRouter
from services.image import upload_image

from starlette.responses import RedirectResponse

router = APIRouter(
    prefix="/",
    responses={404: {"description": "Not found"}},
)

st.title("Upload Image")
user_id = st.text_input("Enter user ID")
uuid = st.text_input("Enter UUID")
upload_file = st.file_uploader("Upload Files", type=["jpg", "png"])

if upload_file is not None:
    image = Image.open(upload_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.write("")
    st.write("Predicting...")
    image = Image.open(upload_file)
    image = image.convert("RGB")
    image = image.resize((224, 224))
    upload_image(user_id, uuid, image)