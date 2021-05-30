# Keras neural network environment test

from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Flatten
from keras.layers import Dense
import numpy as np
import time

#training data company name
name = 'activision'
#number of days per row
ndays = 2

#load the dataset, using AAPL data from 2013-2018
dataset = loadtxt('../Data/diabetes_data.txt', delimiter=',')
print("Dataset len: " + str(len(dataset)))
#split into input X and output Y, ndays is number of days per row

x = dataset[:,0:2*ndays] #columns 0->ndays-1
y = dataset[:,2*ndays] #column ndays

print(x)
accuracy_mean = 0
n = 1

#measure time in seconds
start = time.time()
for i in range(n):
    #define Keras model
    model = Sequential()
    model.add(Dense(20, input_dim=2*ndays, activation='relu', name = 'input')) #1a layer, 12 nodes, ReLU activation functions
    model.add(Dense(5, activation='relu', name = 'first_layer')) #2a layer, 8 nodes
    #model.add(Flatten()) #testing flatten layer
    model.add(Dense(1, activation='sigmoid', name = 'last_layer')) #3a layer, Sigmoid activation function for output in [0,1]

    print(model.get_layer(name='input').input_shape[1]) #number of inputs

    #compile Keras model, Cross Entropy loss function for binary classification, Adam algorithm for optimization
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    #fit (train) the Keras model on the dataset
    model.fit(x,y, epochs=10, batch_size=10, verbose=1)

    #evaluate Keras model
    _, accuracy = model.evaluate(x, y, verbose=0)
    print('Accuracy (it. %d): %.2f' % (i,accuracy*100))
    accuracy_mean += accuracy

    #save model to file if acc >98
    """if accuracy>=0.98:
        #save model to json file
        model_json = model.to_json()
        with open("stocks_model_ndays2_e500_b10.json", "w") as json_file:
            json_file.write(model_json)

        #save weights to h5 file
        model.save_weights("stocks_model_ndays2_e500_b10.h5")
        print("Model saved to json file.")
        break"""

#save model
model.save("my_model.h5")
#end timer
end = time.time()
elapsed_time = end-start #in seconds
accuracy_mean = accuracy_mean/n
print(('Accuracy mean: %.2f\nTime: %d seconds' % (accuracy_mean*100, elapsed_time)))

#make class predictions with the model
predictions = model.predict(x)
rounded = [np.round(p) for p in predictions]
#summarize first 5 cases
for i in range(100,120):
    print('%s -> %d (expected %d)' % (x[i].tolist(), rounded[i], y[i]))
