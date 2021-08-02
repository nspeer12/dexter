import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
import math
import pandas as pd
import json
import nltk
from nltk.stem import WordNetLemmatizer
import csv

class assistantDataset(Dataset):

    def __init__(self):
        # Load data
        jsonfile = open('intents.json','r')
        jsondata = jsonfile.read()
        intents = json.loads(jsondata)

        lemmatizer = WordNetLemmatizer()
        words = []
        classes = []
        documents = []
        ignore_letters = ['!', '?', ',', '.']

        for intent in intents['intents']:
            for pattern in intent['patterns']:
                word = nltk.word_tokenize(pattern)
                words.extend(word)
                documents.append((word, intent['tag']))
                if intent['tag'] not in classes:
                    classes.append(intent['tag'])

        words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_letters]
        words = sorted(list(set(words)))
        classes = sorted(list(set(classes)))

        # print(words)
        # print(classes)
        # print(documents)

        word_dict = {}
        for i in range(len(words)):
            word_dict[words[i]] = i

        with open("Assistant_features.csv",'w', newline="") as f:
            writer = csv.writer(f)
            for word in word_dict.keys():
                writer.writerow([word])

        with open("Assistant_labels.csv",'w', newline="") as f:
            writer = csv.writer(f)
            for label in classes:
                writer.writerow([label])

        x = []
        y = []

        for doc in documents:
            bag = [0] * len(words)
            word_patterns = doc[0] # extracts features
            word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns] # makes lower case

            for word in word_patterns:
                if word in word_dict:
                    bag[word_dict.get(word)] += 1

            label = classes.index(doc[1])
            x.append(bag)
            y.append(label)
        
        x = np.array(x)
        y = np.array(y)

        self.x = torch.from_numpy(np.array(x))
        self.y = torch.from_numpy(np.array(y))
        self.n_samples = len(y)
        self.num_features = len(words)
        self.num_classes = len(classes)
        

    def __getitem__(self, index):
        return self.x[index], self.y[index]

    def __len__(self):
        return self.n_samples

# dataset = assistantDataset()
# first_data = dataset[0]
# features, labels = first_data
# print(features, labels)

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