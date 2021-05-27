import torch
import torch.nn as nn

class NeuralNet(nn.Module):
    def __init__(self, num_features, num_classes):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(num_features, 64)
        self.relu = nn.ReLU()
        self.l2 = nn.Linear(64, 32)
        self.relu = nn.ReLU()
        self.l3 = nn.Linear(32, num_classes)

    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        return out