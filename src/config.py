import os
import torch
from pydantic import BaseSettings
from models import mobilenet, cmu

class Settings(BaseSettings):
    host: str = "http://127.0.0.1:8000"
    storage_root: str = "images"
    scale_search: list = [0.5, 1.0, 1.5, 2.0]
    box_size: int = 368
    stride: int = 8
    padding_value = 128
    threshold1: float = 0.1
    threshold2: float = 0.05
    window_size: int = 10

def model_load(model_path, device):
    model = mobilenet.PoseEstimationWithMobileNet().to(device)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    print('Mobilenet Model is now successfully loaded...')

    return model

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = model_load('../weights/MobileNet_bodypose_model', device)


settings = Settings()

