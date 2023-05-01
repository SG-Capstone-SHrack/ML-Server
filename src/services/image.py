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
from uuid import UUID

from config import settings
from services.storage import *


router = APIRouter(
    prefix="/image",
    responses={404: {"description": "Not found"}},
)

# get an image from client by POST
@router.post("/upload_image")
async def upload_image(user_id: str, uuid: UUID, file: UploadFile = File(...)):
    '''
    parameters:
        file: image
    return:
        file path
    '''
    
    file_name = save_image_file(user_id, uuid, file)

    return {"filename": file_name}


# get lists of images from client by POST
@router.post("/upload_images")
async def upload_images(user_id: str, uuid: UUID, files: list = File(...)):
    '''
    parameters:
        files: list of images
    return:
        list of file paths
    '''

    file_names = []

    for file in files:
        
        file_name = save_image_file(user_id, uuid, file)
        
        file_names.append(file_name)
    
    return {"filenames": file_names}