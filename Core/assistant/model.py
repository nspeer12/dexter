import re
import os
import time
import numpy as np
import pandas as pd
import random
import string
import torch
import matplotlib.pyplot as plt

if torch.cuda.is_available():    
    device = torch.device("cuda")
    print("GPU")
else:
    print("CPU")
    device = torch.device("cpu")


seed_val = 2020
random.seed(seed_val)
np.random.seed(seed_val)
torch.manual_seed(seed_val)
torch.cuda.manual_seed_all(seed_val)


from transformers import AutoConfig

# Configuring model for later

model_name = "distilbert-base-uncased"
# model_name = "bert-based-cased"
# model_name = "bert-large-cased"
# model_name = "bert-base-uncased"
# model_name = "bert-large-uncased"
# model_name = "xlnet-base-cased"
# model_name = "sshleifer/tiny-distilbert-base-uncased-finetuned-sst-2-english"
# model_name = "ipuneetrathore/bert-base-cased-finetuned-finBERT"

config = AutoConfig.from_pretrained(model_name,
                                    output_attentions = False,
                                    output_hidden_states = False,
                                    num_labels = 2, # binary classification
                                   )


data_file_name = "data/1.5M_tweets.csv"
#df.to_csv(data_file_name, index=False)

df = pd.read_csv(data_file_name)

df = df.rename(columns={"2" : "tweets", "3" : "label"})

# make labels class integers
df["label"] = [1 if x == "Bullish" else 0 for x in df["label"]]

df.head()

from transformers import AutoTokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# take dataframe columns as lists
tweets = df.tweets.values
labels = df.label.values
    
def embed_text(tweets):
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Tokenize words and map to IDs
    input_ids = []

    for tweet in tweets:
        encoded_tweet = tokenizer.encode(
                            tweet,
                            add_special_tokens = True,
                        )

        input_ids.append(encoded_tweet)
    
    max_len = 64

    input_ids = pad_sequences(input_ids, maxlen=max_len, dtype="long", 
                              value=0, truncating="post", padding="post")
    
    # Create attention masks
    attention_masks = []

    # Iterate through tweet word IDs
    for i in input_ids:
        # Create a mask for each tweet
        # 1 if there's a word ID
        # 0 if ID is 0
        mask = [int(token_id > 0) for token_id in i]
        attention_masks.append(mask)
    
    return input_ids, attention_masks

input_ids, attention_masks = embed_text(tweets)


from sklearn.model_selection import train_test_split

# 90/10 Train-test split
train_inputs, validation_inputs, train_labels, validation_labels = train_test_split(input_ids, labels, 
                                                            random_state=2020, test_size=0.1)
# Split attention masks too
train_masks, validation_masks, _, _ = train_test_split(attention_masks, labels,
                                             random_state=2020, test_size=0.1)


# Convert all inputs and labels into torch tensors
train_inputs = torch.tensor(train_inputs)
validation_inputs = torch.tensor(validation_inputs)
train_labels = torch.tensor(train_labels)
validation_labels = torch.tensor(validation_labels)
train_masks = torch.tensor(train_masks)
validation_masks = torch.tensor(validation_masks)

from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler

batch_size = 256

# Create the DataLoader for our training set.
train_data = TensorDataset(train_inputs, train_masks, train_labels)
train_sampler = RandomSampler(train_data)
train_dataloader = DataLoader(train_data, sampler=train_sampler, batch_size=batch_size)

# Create the DataLoader for our validation set.
validation_data = TensorDataset(validation_inputs, validation_masks, validation_labels)
validation_sampler = SequentialSampler(validation_data)
validation_dataloader = DataLoader(validation_data, sampler=validation_sampler, batch_size=batch_size)

from transformers import AutoModelForSequenceClassification, BertForSequenceClassification

model = AutoModelForSequenceClassification.from_config(config)

model.to(device)

from torch.optim import Adam

optimizer = Adam(model.parameters(), lr=0.0001)

epochs = 5

# Total number of training steps is number of batches * number of epochs.
total_steps = len(train_dataloader) * epochs


# Function to calculate the accuracy of our predictions vs labels
def calculate_accuracy(preds, labels):
    pred_flat = np.argmax(preds, axis=1).flatten()
    labels_flat = labels.flatten()
    return np.sum(pred_flat == labels_flat) / len(labels_flat)

from tqdm import tqdm
from torch.utils.tensorboard import SummaryWriter
writer = SummaryWriter()

# for tensorboard
t = 0

for epoch in tqdm(range(0, epochs)):
    
    # --- Training ---
    
    # Total loss for each epoch
    total_loss = 0
    
    # Put model in training mode
    model.train()

    # Unpack and iterate through each batch in training data
    for step, batch in enumerate(train_dataloader):
            
        # batch contains three pytorch tensors:
        #   [0]: input ids 
        #   [1]: attention masks
        #   [2]: labels 
        b_input_ids = batch[0].to(device)
        b_input_mask = batch[1].to(device)
        b_labels = batch[2].to(device)
        
        # clear gradients
        model.zero_grad()
        
        # make predictions on training data
        outputs = model(b_input_ids, 
                    attention_mask=b_input_mask, 
                    labels=b_labels)
        
        # Take loss from training output
        loss = outputs[0]
        
        # Add batch's loss to the total loss of the epoch
        total_loss += loss.item()
        
        writer.add_scalar("Loss/step", loss.item(), t)
        t+=1
        
        # Perform a backward pass to calculate the gradients.
        loss.backward()
        
        # Clip gradients
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        
        # Update model hyperparameters
        optimizer.step()
        
    # --- Validation ---
    
    # Average loss over the epoch
    avg_train_loss = total_loss / len(train_dataloader)            
    
    # Store average loss for the epoch
    writer.add_scalar("Loss/epoch", avg_train_loss, epoch)
    
    # Validate model after training
    model.eval()
    
    # Tracking variables 
    eval_loss, eval_accuracy = 0, 0
    num_eval_steps, num_eval_examples = 0, 0
    
    # Evaluate data for one epoch
    for batch in validation_dataloader:
        
        # Add batch to GPU
        batch = tuple(t.to(device) for t in batch)
        
        # Unpack the inputs from our dataloader
        b_input_ids, b_input_mask, b_labels = batch
        
        # Telling the model not to compute or store gradients, saving time and memory
        with torch.no_grad():        
            # Forward pass, calculate predictions on training data.
            outputs = model(b_input_ids, 
                            attention_mask=b_input_mask)
        
        # Get the "logits" output by the model. The "logits" are the output
        # values prior to applying an activation function like the softmax.
        logits = outputs[0]
        
        # Move logits and labels to CPU
        logits = logits.detach().cpu().numpy()
        label_ids = b_labels.to('cpu').numpy()
        
        tmp_eval_accuracy = calculate_accuracy(logits, label_ids)
        
        eval_accuracy += tmp_eval_accuracy
        
        # Track the number of batches
        num_eval_steps += 1
        
    # Calculate validation accuracy and log to TensorBoard
    accuracy = eval_accuracy / num_eval_steps
    writer.add_scalar("Validation Accuracy", accuracy, epoch)
    
    print("Accuracy: {0:.2f}".format(accuracy))
    
    torch.save(model.state_dict(), "models/model_checkpoint_epoch_" + str(epoch))

model_path = "models/distilBERT_10epochs.pt"
torch.save(model.state_dict(), model_path)


tweets = df.tweets.values
labels = df.label.values

input_ids, attention_masks = embed_text(tweets)
    
prediction_inputs = torch.tensor(input_ids)
prediction_masks = torch.tensor(attention_masks)
prediction_labels = torch.tensor(labels)

batch_size = 64

prediction_data = TensorDataset(prediction_inputs, prediction_masks, prediction_labels)
prediction_sampler = SequentialSampler(prediction_data)
prediction_dataloader = DataLoader(prediction_data, sampler=prediction_sampler, batch_size=batch_size)

# Let's make predictions
model.eval()

predictions = []
true_labels = []

for batch in prediction_dataloader:
    batch = tuple(t.to(device) for t in batch)
  
    b_input_ids, b_input_mask, b_labels = batch
  
    with torch.no_grad():
        outputs = model(b_input_ids,
                        attention_mask=b_input_mask)
        
    logits = outputs[0]
    
    logits = logits.detach().cpu().numpy()
    label_ids = b_labels.to('cpu').numpy()
  
    predictions.append(logits)

    true_labels.append(label_ids)

preds = []
for i in predictions:
    vals = np.argmax(i, axis=1).flatten()
    for v in vals:
        preds.append(v)

labels = []
for l in true_labels:
    for i in l:
        labels.append(i)

from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

# ACCURACY
acc = accuracy_score(labels, preds)
print("Accuracy: {:.3f}".format(acc))

# PRECISION
precision = precision_score(labels, preds)
print("Precision: {:.3f}".format(precision))

# RECALL
recall = recall_score(labels, preds)
print("Recall: {:.3f}".format(recall))

# F1
f1 = f1_score(labels, preds)
print("F1 Score: {:.3f}".format(f1))