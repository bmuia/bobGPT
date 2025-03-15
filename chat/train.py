import torch
import torch.nn as nn
import torch.optim as optim
import json
import random
import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer
from .utils import tokenize, stem, bag_of_words

stemmer = PorterStemmer()

# Load intents dataset
with open('chat/intents.json', 'r') as file:
    intents = json.load(file)

# Neural Network Model
class ChatbotModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(ChatbotModel, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, output_size)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.l1(x))
        x = self.relu(self.l2(x))
        return self.l3(x)

# Training the model
def train():
    all_words = []
    tags = []
    xy = []

    for intent in intents['intents']:
        for pattern in intent['patterns']:
            w = tokenize(pattern)
            all_words.extend(w)
            xy.append((w, intent['tag']))
        if intent['tag'] not in tags:
            tags.append(intent['tag'])

    all_words = sorted(set(stem(w) for w in all_words))
    tags = sorted(tags)

    X_train = []
    y_train = []

    for (pattern_sentence, tag) in xy:
        bag = bag_of_words(pattern_sentence, all_words)
        X_train.append(bag)
        y_train.append(tags.index(tag))

    X_train = np.array(X_train)
    y_train = np.array(y_train)

    input_size = len(X_train[0])
    hidden_size = 8
    output_size = len(tags)
    model = ChatbotModel(input_size, hidden_size, output_size)

    # Training setup
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    epochs = 1000
    for epoch in range(epochs):
        X_tensor = torch.FloatTensor(X_train)
        y_tensor = torch.LongTensor(y_train)

        optimizer.zero_grad()
        output = model(X_tensor)
        loss = criterion(output, y_tensor)
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 100 == 0:
            print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')

    # Save model and metadata
    torch.save({
        'model_state': model.state_dict(),
        'input_size': input_size,
        'hidden_size': hidden_size,
        'output_size': output_size,
        'all_words': all_words,
        'tags': tags
    }, "chat/chatbot_model.pth")

    print("Model training complete. Model saved!")

if __name__ == "__main__":
    train()
