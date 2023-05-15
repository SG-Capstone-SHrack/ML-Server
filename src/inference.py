import os
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
from PIL import Image

from config import settings

from pose_estimator import model_inference

router = APIRouter(
    prefix="/inference",
    responses={404: {"description": "Not found"}},
)

# get an image from client by POST
@router.post("/image/{user_id}/{uuid}")
async def inference_image(
    user_id: str,
    uuid: str,
    file: UploadFile = File(...)):
    '''
    parameters:
        file: image
    return:
        file path
    '''

    file_content = np.array(Image.open(file.file))
    
    result = model_inference(file_content, settings, 'pushup-left-arm')
    
    print(result)

    return result
