import torch
import torch.nn as nn

class NeuralNetM(nn.Module):
    def __init__(self, num_classes):
        super(NeuralNetM, self).__init__()
        self.l1 = nn.Linear(253, 12)
        self.relu = nn.ReLU()
        self.l2 = nn.Linear(12, num_classes)

    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        return out