import torch
import numpy as np
import json
import random
from .train import ChatbotModel
from .utils import tokenize, bag_of_words

# Load intents dataset
with open('chat/intents.json', 'r') as file:
    intents = json.load(file)

# Load trained model
model_data = torch.load("chat/chatbot_model.pth")

input_size = model_data['input_size']
hidden_size = model_data['hidden_size']
output_size = model_data['output_size']
all_words = model_data['all_words']
tags = model_data['tags']

# Initialize model
model = ChatbotModel(input_size, hidden_size, output_size)
model.load_state_dict(model_data['model_state'])
model.eval()

def get_response(message):
    words = tokenize(message)
    bag = bag_of_words(words, all_words)
    X = torch.FloatTensor(bag).unsqueeze(0)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    for intent in intents['intents']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])

    return "I'm not sure I understand."
