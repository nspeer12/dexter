import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from gestureDataLoader import GestureDataset
from gestureModel import NeuralNetG
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import numpy as np
import pandas as pd

# Device Config
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Hyper Parameter
df = pd.read_csv('../../csv/gesture_label.csv',header=None)
num_classes = len(df)
num_epochs = 50
batch_size = 10
learning_rate = 0.001

# Dataset
dataset = GestureDataset()
dataloader = DataLoader(dataset=dataset, batch_size = batch_size, shuffle = True)
print("data loaded")

# import model
model = NeuralNetG(num_classes).to(device)
print("model created")

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
print("loss and optimizer created")

cm = np.zeros((num_classes,num_classes))

# Train the model
n_total_steps = len(dataloader)
for epoch in range(num_epochs):
    for i, (features, labels) in enumerate(dataloader):

        features = features.to(device=device, dtype=torch.float32)
        labels = labels.to(device=device, dtype=torch.long)
        # Forward pass
        outputs = model(features)
        loss = criterion(outputs, labels)
        
        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if (i+1) % 10 == 0:
            print (f'Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{n_total_steps}], Loss: {loss.item():.4f}')

    # Validation Accuracy
    with torch.no_grad():
        n_correct = 0
        n_samples = 0
        for features, labels in dataloader:
            features = features.to(device=device, dtype=torch.float32)
            labels = labels.to(device=device, dtype=torch.long)
            outputs = model(features)

            _, predictions = torch.max(outputs,1)
            n_samples += labels.shape[0]
            n_correct += (predictions == labels).sum().item()

        acc = 100.0* n_correct / n_samples
        print(f'Test accuracy = {acc}')


# Confusion Matrix
with torch.no_grad():
    for features, labels in dataloader:
        features = features.to(device=device, dtype=torch.float32)
        labels = labels.to(device=device, dtype=torch.long)
        outputs = model(features)
        _, predictions = torch.max(outputs,1)


        for i in range(len(labels)):
            cm[labels[i],predictions[i]] = cm[labels[i],predictions[i]] + 1

            if (labels[i] != predictions[i]):
                print("\n\nhello\n\n",labels[i],predictions[i])

# Y is actual X is predicted
print(cm)
                
# Specify Path & Save Model
PATH = "GestureModel.pth"
torch.save(model.state_dict(), PATH)