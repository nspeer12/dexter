import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
import math
import pandas as pd

class GestureDataset(Dataset):

    def __init__(self):
        # Load data
        gesture_label_csv_path = '../../csv/gesture.csv'
        xy = np.loadtxt(gesture_label_csv_path, delimiter=",", dtype = np.float32, skiprows=1)
        self.x = torch.from_numpy(xy[:, 1:])
        self.y = torch.from_numpy(xy[:, 0])
        self.n_samples = xy.shape[0]

    def __getitem__(self, index):
        return self.x[index], self.y[index]

    def __len__(self):
        return self.n_samples

# dataset = GestureDataset()
# # first_data = dataset[0]
# # features, labels = first_data
# # print(features, labels)

# dataloader = DataLoader(dataset=dataset, batch_size = 4, shuffle = True)

# # dataiter = iter(dataloader)
# # data = dataiter.next()
# # features, labels = data
# # print(features, labels)

# # training loop
# num_epochs = 2
# total_samples = len(dataset)
# n_iterations = math.ceil(total_samples / 4)
# print(total_samples, n_iterations)

# for epoch in range(num_epochs):
#     for i, (inputs, labels) in enumerate(dataloader):
#         # forward, backward, update
#         if (i + 1) % 5 == 0:
#             print(f'epoch {epoch + 1}/{num_epochs}, step {i+1} / {n_iterations}, inputs {inputs.shape}')