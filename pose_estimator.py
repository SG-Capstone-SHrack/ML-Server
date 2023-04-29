import os
import numpy as np
import torch
import torch.nn as nn
<<<<<<< HEAD


=======
from config import settings
from models import mobilenet, cmu

box_size = settings.box_size
scale_search = settings.scale_search


def model_load(model, model_path, device):
    model = model.to(device)
    model.load_state_dict(torch.load(model_path))
    model.eval()

    return model


def model_inference(model, input, settings):
    multiplier = [x * box_size / input.shape[0] for x in scale_search]
    heatmap_avg = np.zeros((input.shape[0], input.shape[1], 19))
    paf_avg = np.zeros((input.shape[0], input.shape[1], 38))
>>>>>>> parent of 1327587 (230429 21:47 Minseok)
