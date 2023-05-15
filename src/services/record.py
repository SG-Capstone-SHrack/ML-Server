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

class Record:
    user_records = {}

    @classmethod
    def get_user_records(cls, user_id: str):
        if user_id not in cls.user_records:
            cls.user_records[user_id] = {}

        return cls.user_records[user_id]
    
    @classmethod
    def get_user_records_by_uuid(cls, user_id: str, uuid: str):
        if user_id not in cls.user_records:
            cls.user_records[user_id] = {}

        return cls.user_records[user_id][uuid]


    @classmethod
    def add_user_record(cls, user_id: str, uuid: str, angle: float):
        if user_id not in cls.user_records:
            cls.user_records[user_id] = {}

        if uuid not in cls.user_records[user_id]:
            cls.user_records[user_id][uuid] = []

        cls.user_records[user_id][uuid].append(angle)


    @classmethod
    def delete_user_records(cls, user_id: str, uuid: str):
        '''
        delete user files to keep the size of list to window_size (default: 10)

        :param user_id: user id
        :param uuid: uuid
        :return: True if success, False if fail

        '''
        if user_id not in cls.user_records:
            return False
        
        if uuid not in cls.user_records[user_id]:
            return False
        
        # only remaining maximum window_size files
        if len(cls.user_records[user_id][uuid]) > settings.window_size:
            cls.user_records[user_id][uuid] = cls.user_records[user_id][uuid][-settings.window_size:]
        
        return True


records = Record()