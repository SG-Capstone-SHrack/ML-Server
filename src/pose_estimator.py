import os
import numpy as np
import torch
import torch.nn as nn
import cv2
import matplotlib.pyplot as plt
import time

# from config import settings
from utils.util import *
from models import mobilenet, cmu
from utils.find_peaks_running import RealtimePeakDetector
# box_size = settings.box_size
# scale_search = settings.scale_search

def Net_Prediction(model, image, device, backbone = 'Mobilenet'):
    scale_search = [1]
    stride = 8
    padValue = 128
    heatmap_avg = np.zeros((image.shape[0], image.shape[1], 19))
    paf_avg = np.zeros((image.shape[0], image.shape[1], 38))
    
    for m in range(len(scale_search)):
        scale = scale_search[m]
        imageToTest = cv2.resize(image, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

        # pad right and down corner to make sure image size is divisible by 8
        imageToTest_padded, pad = padRightDownCorner(imageToTest, stride, padValue)
        im = np.transpose(np.float32(imageToTest_padded), (2, 0, 1)) / 256 - 0.5
        # ascontiguousarray 함수는 메모리에 연속적으로 저장되지 않는 배열을 연속적으로 저장되는 배열로 변환하기 때문에 더 빠르게 데이터를 불러올 수 있음
        im = np.ascontiguousarray(im)
        data = torch.from_numpy(im).float().unsqueeze(0).to(device)
   
        with torch.no_grad():
            if backbone == 'CMU':
                Mconv7_stage6_L1, Mconv7_stage6_L2 = model(data)
                _paf = Mconv7_stage6_L1.cpu().numpy()
                _heatmap = Mconv7_stage6_L2.cpu().numpy()
            elif backbone == 'Mobilenet':
                stages_output = model(data)
                _paf = stages_output[-1].cpu().numpy()
                _heatmap = stages_output[-2].cpu().numpy()  
            
        # extract outputs, resize, and remove padding
        heatmap = np.transpose(np.squeeze(_heatmap), (1, 2, 0))  # output 1 is heatmaps
        heatmap = cv2.resize(heatmap, (0, 0), fx=stride, fy=stride, interpolation=cv2.INTER_CUBIC)
        heatmap = heatmap[:imageToTest_padded.shape[0] - pad[2], :imageToTest_padded.shape[1] - pad[3], :]
        heatmap = cv2.resize(heatmap, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_CUBIC)
        # print(heatmap.shape)
        
        paf = np.transpose(np.squeeze(_paf), (1, 2, 0))  # output 0 is PAFs
        paf = cv2.resize(paf, (0, 0), fx=stride, fy=stride, interpolation=cv2.INTER_CUBIC)
        paf = paf[:imageToTest_padded.shape[0] - pad[2], :imageToTest_padded.shape[1] - pad[3], :]
        paf = cv2.resize(paf, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_CUBIC)
        # print(paf.shape)
        
        heatmap_avg += heatmap / len(scale_search)
        paf_avg += paf / len(scale_search)
        
    return heatmap_avg, paf_avg

def model_load(model_path, device):
    model = mobilenet.PoseEstimationWithMobileNet().to(device)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    print('Mobilenet Model is now successfully loaded...')

    return model


def model_inference(model, device, input, settings, exercise_type):
    scale = 1

    # load image
    image_to_test = cv2.resize(input, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    since = time.time()

    heatmap, paf = Net_Prediction(model, image_to_test, device, backbone = 'Mobilenet')
    t1 = time.time()
    print("Model inference in {:2.3f} seconds".format(t1 - since))

    all_peaks = peaks(heatmap, 0.1)

    t2 = time.time()
    print("Find peaks in {:2.3f} seconds".format(t2 - t1))

    #canvas = draw_part(image, all_peaks, show, scale)
    connection_all, special_k = connection(all_peaks, paf, image_to_test)
    t2 = time.time()
    print("Find connections in {:2.3f} seconds".format(t2 - t1))
    candidate, subset = merge(all_peaks, connection_all, special_k)
    t3 = time.time()
    print("Merge in {:2.3f} seconds".format(t3 - t2))

    angle_btw = draw_bodypose(image, candidate, subset, exercise_type, scale)

    print("Total inference in {:2.3f} seconds".format(time.time() - since))
    # plt.imshow(canvas[:,:, [2,1,0]])
    # plt.axis('off')
    # plt.savefig('inferenced_test.jpg')
    
    return angle_btw

if __name__ == '__main__':
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = model_load('../weights/MobileNet_bodypose_model', device)

    for i in range(10):
        image_path = './images/pushup_up.jpg'
        image = cv2.imread(image_path)
        settings = 0

        angle = model_inference(model, device, image, settings, "pushup-right-arm")
        print("Angle_btw: {:2.3f}".format(angle))



    # multiplier = [x * box_size / input.shape[0] for x in scale_search]
    # heatmap_avg = np.zeros((input.shape[0], input.shape[1], 19))
    # paf_avg = np.zeros((input.shape[0], input.shape[1], 38))
