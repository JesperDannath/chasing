#Reinforcement Learning:
#1. Interactive Network. Sending back results to input
#2. Sampling from the Probabilities for action (no maximum approach, introduce experiment)
#3. Our fake-target-function will be the sampled outcome

#Model für den Agenten der Verfolgt:
import tensorflow.keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.optimizers import SGD, Adam
import numpy as np

#Buildung the Model
def build_model():
    model = Sequential()
    model.add(Dense(20, activation="relu", input_shape=(6,)))
    model.add(Dense(20, activation="relu",input_shape=(8,)))
    model.add(Dense(1, input_shape=(8,)))
    
    #Compiling the Model
    #sgd = SGD(lr=0.01)
    adam = Adam(learning_rate=0.001)
    model.compile(optimizer=adam,
                  loss='mean_squared_error',
                  metrics=["acc"])

    return(model)

model = build_model()
#Examples for usage of Model
#model.fit([[0,0,0,0]], [1])
#model.predict([[0,0,0,0]])


