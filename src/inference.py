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
from services.record import records

from pose_estimator import model_inference

router = APIRouter(
    prefix="/inference",
    responses={404: {"description": "Not found"}},
)

# get an image from client by POST
@router.post("/image/{user_id}/{uuid}/{exercise_type}")
async def inference_image(
    user_id: str,
    uuid: str,
    exercise_type: str,
    file: UploadFile = File(...)):
    '''
    parameters:
        file: image
    return:
        file path
    '''

    file_content = np.array(Image.open(file.file))
    
    result = model_inference(file_content, settings, exercise_type)
    
    records.add_user_record(user_id, uuid, result)
    user_records = records.get_user_records_by_uuid(user_id, uuid)
    
    print(user_records)

    return {
        "user_id": user_id,
        "uuid": uuid,
        "exercise_type": exercise_type,
        "angle": result, "user_records": user_records
        }

