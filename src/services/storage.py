import os
import json
import datetime
import numpy as np

from typing import Optional
from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from importlib import import_module
from uuid import UUID

from config import settings

class StroageFile:
    user_files: dict

    def __init__(self):
        self.user_files = {}

    @classmethod
    def get_user_files(cls, user_id: str):
        if user_id not in cls.user_files:
            cls.user_files[user_id] = {}

        return cls.user_files[user_id]
    
    @classmethod
    def get_user_files_by_uuid(cls, user_id: str, uuid: UUID):
        if user_id not in cls.user_files:
            cls.user_files[user_id] = {}

        return cls.user_files[user_id][uuid]


    @classmethod
    def add_user_file(cls, user_id: str, uuid: UUID, file_path: str):
        if user_id not in cls.user_files:
            cls.user_files[user_id] = {}

        if uuid not in cls.user_files[user_id]:
            cls.user_files[user_id][uuid] = []

        cls.user_files[user_id][uuid].append({
            'file_path': file_path,
            'file_name': os.path.basename(file_path),
            'datetime': datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        })


    @classmethod
    def delete_user_file(cls, user_id: str, uuid: UUID):
        '''
        delete user files to keep the size of list to window_size (default: 10)

        :param user_id: user id
        :param uuid: uuid
        :return: True if success, False if fail

        '''
        if user_id not in cls.user_files:
            return False
        
        if uuid not in cls.user_files[user_id]:
            return False
        
        # only remaining maximum window_size files
        if len(cls.user_files[user_id][uuid]) > settings.window_size:
            for i in range(len(cls.user_files[user_id][uuid]) - settings.window_size):
                file_path = cls.user_files[user_id][uuid][i]['file_path']

                if os.path.exists(file_path):
                    os.remove(file_path)
            
            cls.user_files[user_id][uuid] = cls.user_files[user_id][uuid][-settings.window_size:]
        
        return True


stroageFile = StroageFile()

def get_stroage_file_path(user_id: str, file_name: str) -> str:
    user_storage_path = os.path.join(settings.storage_root, user_id)

    if not os.path.exists(user_storage_path):
        os.makedirs(user_storage_path)

    if os.path.exists(os.path.join(user_storage_path, file_name)):
        return False
    
    return os.path.join(user_storage_path, file_name)


def save_image_file(user_id: str, uuid: UUID, file_content: any) -> bool:
    '''
    save image file from client

    :param user_id: user id
    :param uuid: uuid
    :param file_content: file content
    :return: file name
    '''
    file_name = datetime.datetime.now().strftime("%y%m%d_%H%M%S") + "1"

    # rename it by adding a number if there is already a file with the same name
    while True:
        file_path = get_stroage_file_path(user_id, file_name)

        if file_path:
            break

        file_name = datetime.datetime.now().strftime("%y%m%d_%H%M%S") + str(int(file_name[-1]) + 1)

    # extension with jpg by default if there is no extension
    if not file_path.endswith(".jpg"):
        file_path += ".jpg"

    with open(file_path, "wb") as buffer:
        buffer.write(file_content)

    StroageFile.add_user_file(user_id, uuid, file_path)

    return file_name