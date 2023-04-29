import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    host: str = "http://127.0.0.1:8000"
    image_dir: str = "images"
    scale_search: list = [0.5, 1.0, 1.5, 2.0]
    box_size: int = 368
    stride: int = 8
    padding_value = 128
    threshold1: float = 0.1
    threshold2: float = 0.05

settings = Settings()
