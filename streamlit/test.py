import io
import requests
import streamlit as st

from PIL import Image

# from services.image import upload_image
from requests_toolbelt.multipart.encoder import MultipartEncoder
from starlette.responses import RedirectResponse

api_host = "http://0.0.0.0:8080"

def upload_image(user_id, uuid, exercise_type, image):
    '''
    parameters:
        user_id: user id
        uuid: uuid
        image: image
    return:
        file path
    '''
    
    url = f"{api_host}/inference/image/{user_id}/{uuid}/{exercise_type}"

    files = {
        'file': image
    }

    response = requests.post(
        url, 
        files=files
    )
    return response.json()
    


st.title("Upload Image")
user_id = st.text_input("Enter user ID")
uuid = st.text_input("Enter UUID")
exercise_type = st.selectbox(
    'Select exercise type',
    ('squat-right-leg', 'squat-left-leg', 'pushup-right-arm', 'pushup-left-arm')
)
upload_file = st.file_uploader("Upload Files", type=["jpg", "png"])

if upload_file is not None:
    # image = Image.open(upload_file)
    st.image(upload_file, caption="Uploaded Image", use_column_width=True)
    st.write("")
    st.write("Predicting...")
    # image = Image.open(upload_file)
    # image = image.convert("RGB")
    # image = image.resize((224, 224))

    ret = upload_image(user_id, uuid, exercise_type, upload_file.getvalue())
    st.write(ret)