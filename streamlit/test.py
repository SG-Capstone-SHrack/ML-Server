import requests
import streamlit as st

from PIL import Image

# from services.image import upload_image

from starlette.responses import RedirectResponse
from requests_toolbelt.multipart.encoder import MultipartEncoder

api_host = "http://34.69.53.183/api"

def upload_image(user_id, uuid, image):
    '''
    parameters:
        user_id: user id
        uuid: uuid
        image: image
    return:
        file path
    '''
    
    url = f"{api_host}/image/upload_image"
    
    data = MultipartEncoder(
        fields={
            "user_id": user_id,
            "uuid": uuid,
            "file": image
        }
    )

    response = requests.post(
        url, data=data, headers={"Content-Type": data.content_type}
    )

    return response.json()
    


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
    # upload_image(user_id, uuid, image)

    upload_image(user_id, uuid, image)