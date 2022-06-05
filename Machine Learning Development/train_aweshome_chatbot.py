# -*- coding: utf-8 -*-
"""train_aweshome_chatbot

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rf-O-Ub-aH6N2mPPtZLeOvUmbb_VWcAx

## **About Aweshome**

Aweshome is a chatbot created by implementing machine learning in it. Its manufacture is carried out as an additional feature that will complement the smart home application created that also called Aweshome.
This application has a motto:

***Aweshome: Make your home smart and awesome ***

The chatbot feature will help users explicitly manage the appliances in their house, as well as to know the condition of their house.

## **Steps to create Aweshome Chatbot**

The following is an overview of the steps taken to create an Aweshome chatbot:
1. Prepare the required packages, including the Deep Learning, Tensorflow, Keras, Pickle, and NLTK (Natural Language Processing Toolkit) libraries.
2. Prepare a dataset in the form of a collection of user input and output that must be displayed in response to the Aweshome chatbot. The file is saved in JSON type and is named "intents."
3. Perform data preparation including import required packages, load the JSON file and extract the required data.
4. Creating models including training and testing models.
5. Integrating Aweshome chatbot with application.
"""

#importing the libraries
import json 
import numpy as np 
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder

#importing the dataset
with open('sample_data/intents.json') as file:
    data = json.load(file)

#getting all the data to lists
training_sentences = []
training_labels = []
labels = []
responses = []


for intent in data['intents']:
    for pattern in intent['patterns']:
        training_sentences.append(pattern)
        training_labels.append(intent['tag'])
    responses.append(intent['responses'])
    
    if intent['tag'] not in labels:
        labels.append(intent['tag'])
        
num_classes = len(labels)

#
lbl_encoder = LabelEncoder()
lbl_encoder.fit(training_labels)
training_labels = lbl_encoder.transform(training_labels)

#
vocab_size = 1000
embedding_dim = 16
max_len = 20
oov_token = "<OOV>"

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token) # adding out of vocabulary token
tokenizer.fit_on_texts(training_sentences)
word_index = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(training_sentences)
padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len)

#printing the data
data

#creating the model

model = Sequential()
model.add(Embedding(vocab_size, embedding_dim, input_length=max_len))
model.add(GlobalAveragePooling1D())
model.add(Dense(16, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(num_classes, activation='softmax'))

#compiling the model
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

#view model summary
model.summary()

#training the model
epochs = 550
history = model.fit(padded_sequences, np.array(training_labels), epochs=epochs)

# saving model
model.save("chat_model")

import pickle

# saving tokenizer
with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    

# saving label encoder
with open('label_encoder.pickle', 'wb') as ecn_file:
    pickle.dump(lbl_encoder, ecn_file, protocol=pickle.HIGHEST_PROTOCOL)