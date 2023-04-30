import os
import cv2
import math
import datetime
import numpy as np

from fastapi import APIRouter, FastAPI, HTTPException, \
    Depends, Form, Request, UploadFile, File, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from pydantic import BaseModel

from config import settings


router = APIRouter(
    prefix="/image",
    responses={404: {"description": "Not found"}},
)

# get an image from client by POST
@router.post("/upload_image")
async def upload_image(file: UploadFile = File(...)):
    '''
    parameters:
        file: image
    return:
        file path
    '''
    file_name = datetime.datetime.now().strftime("%y%m%d_%H%M%S") + "1"

    # rename it by adding a number if there is already a file with the same name
    while os.path.exists(os.path.join(settings.storage_root, file_name)):
        file_name = datetime.datetime.now().strftime("%y%m%d_%H%M%S") + str(int(file_name[-1]) + 1)

    file_path = os.path.join(settings.storage_root, file_name)
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    return {"filename": file_name}


# get lists of images from client by POST
@router.post("/upload_images")
async def upload_images(files: list = File(...)):
    '''
    parameters:
        files: list of images
    return:
        list of file paths
    '''
    file_names = []
    for file in files:
        
        file_name = datetime.datetime.now().strftime("%y%m%d_%H%M%S") + "1"

        # rename it by adding a number if there is already a file with the same name
        while os.path.exists(os.path.join(settings.storage_root, file_name)):
            file_name = datetime.datetime.now().strftime("%y%m%d_%H%M%S") + str(int(file_name[-1]) + 1)

        file_path = os.path.join(settings.storage_root, file_name)

        # extension with jpg by default if there is no extension
        if not file_path.endswith(".jpg"):
            file_path += ".jpg"
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        file_names.append(file_name)
    
    return {"filenames": file_path}