import os
import json
import numpy as np

from typing import Optional
from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from importlib import import_module

from config import settings

class StroageFile:
    user_id: str
    file_name: str
    file_path: str


    def __init__(self, user_id: str, file_name: str, file_path: str):
        self.user_id = user_id
        self.file_name = file_name
        self.file_path = file_path


class StroageFileRequestModel(BaseModel):
    user_id: str
    user_file_name: str
    user_file_path: str


def get_stroage_file_path(user_id: str, file_name: str) -> str:
    user_storage_path = os.path.join(settings.storage_root, user_id)
    if not os.path.exists(user_storage_path):
        os.makedirs(user_storage_path)
    return os.path.join(user_storage_path, file_name)



def delete_storage_file(user_id: str, file_name: str) -> bool:
    file_path = get_stroage_file_path(user_id, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False