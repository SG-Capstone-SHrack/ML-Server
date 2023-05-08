import time 
import torch
import torch.nn as nn

from models import mobilenet, cmu

if __name__ == "__main__":    
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    input = torch.Tensor(2, 3, 368, 368).to(device)

    model_CMU = cmu.bodypose_model().to(device)
    model_CMU.load_state_dict(torch.load('weights/bodypose_model'))
    model_CMU.eval()
    
    model_Mobilenet = mobilenet.PoseEstimationWithMobileNet().to(device)
    model_Mobilenet.load_state_dict(torch.load('weights/MobileNet_bodypose_model'))
    model_Mobilenet.eval()
    
    since = time.time()
    
    PAF_CMU, Heatmap_CMU = model_CMU(input)
    print('CMU PAF shape and Heatmap shape', PAF_CMU.shape, Heatmap_CMU.shape)
    t1 = time.time()
    print('CMU Inference time is {:2.3f} seconds'.format(t1 - since))
    
    stages_output= model_Mobilenet(input)
    PAF_Mobilenet, Heatmap_Mobilenet = stages_output[-1], stages_output[-2]
    print('Mobilenet PAF shape and Heatmap shape', PAF_Mobilenet.shape, Heatmap_Mobilenet.shape)
    print('Mobilenet Inference time is {:2.3f} seconds'.format(time.time() - t1))