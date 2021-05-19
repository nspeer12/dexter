import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
import math
import pandas as pd

class MotionDataset(Dataset):

    def __init__(self):
        # Load data
        gesture_label_csv_path = '../../csv/motion.csv'
        xy = np.loadtxt(gesture_label_csv_path, delimiter=",", dtype = np.float32, skiprows=1)
        self.x = torch.from_numpy(xy[:, 1:])
        self.y = torch.from_numpy(xy[:, 0])
        self.n_samples = xy.shape[0]

    def __getitem__(self, index):
        return self.x[index], self.y[index]

    def __len__(self):
        return self.n_samples