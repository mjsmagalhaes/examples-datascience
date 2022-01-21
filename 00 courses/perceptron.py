# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 13:14:35 2022

@author: PICHAU
"""
import numpy as np

# i = np.array([1,7,5])
# w = np.array([0.8, 0.1, 0])

i = np.array([[0, 0],[0,1],[1,0],[1,1]])
w = np.array([0, 0])
# o = np.array([0, 0, 0, 1])
o = np.array([[0], [1], [1], [0]])

def step(v):
    return np.vectorize(lambda x: 1 if x >= 1 else 0)(v)

def sigmoid(v):
    return 1 / (1 + np.exp(-v))

def sigmoid_derivative(v):
    return v * (1-v)

def identity(v):
    return v

def perceptron(input, weights, activation=step):
    return activation(input.dot(weights))
    #return input.dot(weights)

def fit(i, w, o, f=step):
    lRate = 0.1
    totalError = 1;

    while(totalError > 0):
        pred = perceptron(i, w, f)
        error = abs(o - pred)
        totalError = sum(error)
        w = w + (lRate *  error.dot(i))
        print(totalError)

    return w

# def feedforward():


#w = fit(i, w, o)
# print(w)
epochs = 100000
m = 1
lRate = 0.6

# w_1 =  np.array([[-.424, -.740, -.961],[.358, -.577, -.469]])
w_1 = (2 * np.random.random((2,3))) - 1
# w_2 = np.array([[-.017], [-.893], [.148]])
w_2 = (2 * np.random.random((3,1))) - 1

for j in range(epochs):
    layer_1 = perceptron(i, w_1, sigmoid)
    layer_2 = perceptron(layer_1, w_2, sigmoid)

    error = o - layer_2
    if j % 1000 == 0:
        print('{:d} {:.03f}'.format(j, np.mean(abs(error))))

    # Backpropagation
    delta_2 = error * sigmoid_derivative(layer_2)
    dSig = sigmoid_derivative(layer_1)
    delta_1 =  dSig * w_2.T * delta_2

    w_2 = (w_2 * m) + (lRate * layer_1.T.dot(delta_2))
    w_1 = (w_1 * m) + (lRate * i.T.dot(delta_1))


layer_1 = perceptron(i, w_1, sigmoid)
layer_2 = perceptron(layer_1, w_2, sigmoid)