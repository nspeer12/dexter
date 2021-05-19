import torch
from model.gesture.gestureModel import NeuralNet

GESTURE_PATH = "model/gesture/GestureModel.pth"

Model = NeuralNet()
Model.load_state_dict(torch.load(GESTURE_PATH))
Model.eval()

print(Model.state_dict())