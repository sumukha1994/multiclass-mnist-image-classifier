'''
This file implements a multi layer neural network for a multiclass classifier

Hemanth Venkateswara
hkdv1@asu.edu
Oct 2018
'''
import numpy as np
from load_mnist import mnist, one_hot
import matplotlib.pyplot as plt
import pdb
import sys, ast


def relu(Z):
    '''
    computes relu activation of Z

    Inputs:
        Z is a numpy.ndarray (n, m)

    Returns:
        A is activation. numpy.ndarray (n, m)
        cache is a dictionary with {"Z", Z}
    '''
    A = np.maximum(0, Z)
    cache = {}
    cache["Z"] = Z
    return A, cache


def relu_der(dA, cache):
    '''
    computes derivative of relu activation

    Inputs:
        dA is the derivative from subsequent layer. numpy.ndarray (n, m)
        cache is a dictionary with {"Z", Z}, where Z was the input
        to the activation layer during forward propagation

    Returns:
        dZ is the derivative. numpy.ndarray (n,m)
    '''
    dZ = np.array(dA, copy=True)
    Z = cache["Z"]
    dZ[Z<0]=0
    return dZ


def linear(Z):
    '''
    computes linear activation of Z
    This function is implemented for completeness

    Inputs:
        Z is a numpy.ndarray (n, m)

    Returns:
        A is activation. numpy.ndarray (n, m)
        cache is a dictionary with {"Z", Z}
    '''
    A = Z
    cache = {}
    return A, cache


def linear_der(dA, cache):
    '''
    computes derivative of linear activation
    This function is implemented for completeness

    Inputs:
        dA is the derivative from subsequent layer. numpy.ndarray (n, m)
        cache is a dictionary with {"Z", Z}, where Z was the input
        to the activation layer during forward propagation

    Returns:
        dZ is the derivative. numpy.ndarray (n,m)
    '''
    dZ = np.array(dA, copy=True)
    return dZ


def softmax_cross_entropy_loss(Z, Y):
    '''
    Computes the softmax activation of the inputs Z
    Estimates the cross entropy loss

    Inputs:
        Z - numpy.ndarray (n, m)
        Y - numpy.ndarray (1, m) of labels
            when y=[] loss is set to []

    Returns:
        A - numpy.ndarray (n, m) of softmax activations
        cache -  a dictionary to store the activations later used to estimate derivatives
        loss - cost of prediction
    '''
    ### CODE HERE
    Y = Y.astype(int)
    m = np.float64(Y.shape[1])
    int_m = Y.shape[1]
    onehot_y = np.zeros(shape=(10, int(m)))
    onehot_y[Y, range(int_m)] = 1
    mz = np.float64(np.max(Z))
    exp1 = np.exp(Z - mz)
    exp2 = np.sum(np.exp(Z - mz), keepdims=True, axis=0)
    A = np.divide(exp1, exp2)
    indices = np.argmax(onehot_y, axis=1).astype(int)
    prob = A[np.arange(len(A)), indices]
    log_preds = np.log(prob)
    loss = -1.0 * np.sum(log_preds) / len(log_preds)

    return A, loss


def softmax_cross_entropy_loss_der(A, Y):
    '''
    Computes the derivative of softmax activation and cross entropy loss

    Inputs:
        Y - numpy.ndarray (1, m) of labels
        cache -  a dictionary with cached activations A of size (n,m)

    Returns:
        dZ - numpy.ndarray (n, m) derivative for the previous layer
    '''
    ### CODE HERE
    Y = Y.astype(int)
    m = Y.shape[1]
    onehot_y = np.zeros(shape=(10, int(m)))
    onehot_y[Y, range(m)] = 1

    dZ = A - onehot_y
    return dZ


def initialize_multilayer_weights(net_dims):
    '''
    Initializes the weights of the multilayer network

    Inputs:
        net_dims - tuple of network dimensions

    Returns:
        dictionary of parameters
    '''
    np.random.seed(0)
    numLayers = len(net_dims)
    parameters = {}
    for l in range(numLayers - 1):
        parameters["W" + str(l + 1)] = np.multiply(np.float64(0.01), np.random.randn(net_dims[l + 1], net_dims[l]))
        parameters["b" + str(l + 1)] = np.multiply(np.float64(0.01), np.random.randn(net_dims[l + 1], 1))
    return parameters


def linear_forward(A, W, b):
    '''
    Input A propagates through the layer
    Z = WA + b is the output of this layer.

    Inputs:
        A - numpy.ndarray (n,m) the input to the layer
        W - numpy.ndarray (n_out, n) the weights of the layer
        b - numpy.ndarray (n_out, 1) the bias of the layer

    Returns:
        Z = WA + b, where Z is the numpy.ndarray (n_out, m) dimensions
        cache - a dictionary containing the inputs A
    '''
    ### CODE HERE
    Z = np.dot(W, A) + b
    cache = {}
    cache["A"] = A
    return Z, cache


def layer_forward(A_prev, W, b, activation):
    '''
    Input A_prev propagates through the layer and the activation

    Inputs:
        A_prev - numpy.ndarray (n,m) the input to the layer
        W - numpy.ndarray (n_out, n) the weights of the layer
        b - numpy.ndarray (n_out, 1) the bias of the layer
        activation - is the string that specifies the activation function

    Returns:
        A = g(Z), where Z = WA + b, where Z is the numpy.ndarray (n_out, m) dimensions
        g is the activation function
        cache - a dictionary containing the cache from the linear and the nonlinear propagation
        to be used for derivative
    '''
    Z, lin_cache = linear_forward(A_prev, W, b)
    if activation == "relu":
        A, act_cache = relu(Z)
    elif activation == "linear":
        A, act_cache = linear(Z)

    cache = {}
    cache["lin_cache"] = lin_cache
    cache["act_cache"] = act_cache
    return A, cache


def multi_layer_forward(X, parameters):
    '''
    Forward propgation through the layers of the network

    Inputs:
        X - numpy.ndarray (n,m) with n features and m samples
        parameters - dictionary of network parameters {"W1":[..],"b1":[..],"W2":[..],"b2":[..]...}
    Returns:
        AL - numpy.ndarray (c,m)  - outputs of the last fully connected layer before softmax
            where c is number of categories and m is number of samples in the batch
        caches - a dictionary of associated caches of parameters and network inputs
    '''
    L = len(parameters) // 2
    A = X
    caches = []
    for l in range(1, L):  # since there is no W0 and b0
        A, cache = layer_forward(A, parameters["W" + str(l)], parameters["b" + str(l)], "relu")
        caches.append(cache)

    AL, cache = layer_forward(A, parameters["W" + str(L)], parameters["b" + str(L)], "linear")
    caches.append(cache)
    return AL, caches


def linear_backward(dZ, cache, W, b):
    '''
    Backward prpagation through the linear layer

    Inputs:
        dZ - numpy.ndarray (n,m) derivative dL/dz
        cache - a dictionary containing the inputs A, for the linear layer
            where Z = WA + b,
            Z is (n,m); W is (n,p); A is (p,m); b is (n,1)
        W - numpy.ndarray (n,p)
        b - numpy.ndarray (n, 1)

    Returns:
        dA_prev - numpy.ndarray (p,m) the derivative to the previous layer
        dW - numpy.ndarray (n,p) the gradient of W
        db - numpy.ndarray (n, 1) the gradient of b
    '''
    A = cache["A"]
    m = np.float64(A.shape[1])
    dW = np.multiply((1 / m), np.dot(dZ, A.T))
    db = np.multiply((1 / m), np.sum(dZ, axis=1, keepdims=True))
    dA_prev = np.dot(W.T, dZ)
    ## CODE HERE
    return dA_prev, dW, db


def layer_backward(dA, cache, W, b, activation):
    '''
    Backward propagation through the activation and linear layer

    Inputs:
        dA - numpy.ndarray (n,m) the derivative to the previous layer
        cache - dictionary containing the linear_cache and the activation_cache
        activation - activation of the layer
        W - numpy.ndarray (n,p)
        b - numpy.ndarray (n, 1)

    Returns:
        dA_prev - numpy.ndarray (p,m) the derivative to the previous layer
        dW - numpy.ndarray (n,p) the gradient of W
        db - numpy.ndarray (n, 1) the gradient of b
    '''
    lin_cache = cache["lin_cache"]
    act_cache = cache["act_cache"]

    if activation == "relu":
        dZ = relu_der(dA, act_cache)
    elif activation == "linear":
        dZ = linear_der(dA, act_cache)
    dA_prev, dW, db = linear_backward(dZ, lin_cache, W, b)
    return dA_prev, dW, db


def multi_layer_backward(dAL, caches, parameters):
    '''
    Back propgation through the layers of the network (except softmax cross entropy)
    softmax_cross_entropy can be handled separately

    Inputs:
        dAL - numpy.ndarray (n,m) derivatives from the softmax_cross_entropy layer
        caches - a dictionary of associated caches of parameters and network inputs
        parameters - dictionary of network parameters {"W1":[..],"b1":[..],"W2":[..],"b2":[..]...}

    Returns:
        gradients - dictionary of gradient of network parameters
            {"dW1":[..],"db1":[..],"dW2":[..],"db2":[..],...}
    '''
    L = len(caches)  # with one hidden layer, L = 2
    gradients = {}
    dA = dAL
    activation = "linear"
    for l in reversed(range(1, L + 1)):
        dA, gradients["dW" + str(l)], gradients["db" + str(l)] = \
            layer_backward(dA, caches[l - 1], \
                           parameters["W" + str(l)], parameters["b" + str(l)], \
                           activation)
        activation = "relu"
    return gradients


def classify(X, parameters):
    '''
    Network prediction for inputs X

    Inputs:
        X - numpy.ndarray (n,m) with n features and m samples
        parameters - dictionary of network parameters
            {"W1":[..],"b1":[..],"W2":[..],"b2":[..],...}
    Returns:
        YPred - numpy.ndarray (1,m) of predictions
    '''
    ### CODE HERE
    # Forward propagate X using multi_layer_forward
    # Get predictions using softmax_cross_entropy_loss
    # Estimate the class labels using predictions
    Z, cache = multi_layer_forward(X, parameters)
    mz = np.float64(np.max(Z))
    AL = np.divide(np.exp(Z - mz), np.sum(np.exp(Z - mz), keepdims=True, axis=0))
    AL = np.argmax(AL, axis=0)
    return AL


def update_parameters(parameters, gradients, epoch, learning_rate, decay_rate=0.0):
    '''
    Updates the network parameters with gradient descent

    Inputs:
        parameters - dictionary of network parameters
            {"W1":[..],"b1":[..],"W2":[..],"b2":[..],...}
        gradients - dictionary of gradient of network parameters
            {"dW1":[..],"db1":[..],"dW2":[..],"db2":[..],...}
        epoch - epoch number
        learning_rate - step size for learning
        decay_rate - rate of decay of step size - not necessary - in case you want to use
    '''
    alpha = learning_rate * (1 / (1 + decay_rate * epoch))
    L = len(parameters) // 2
    for l in range(L):
        parameters["W" + str(l + 1)] -= alpha * gradients["dW" + str(l + 1)]
        parameters["b" + str(l + 1)] -= alpha * gradients["db" + str(l + 1)]
    return parameters, alpha


def multi_layer_network(X, Y, val_data, val_label, net_dims, num_iterations=500, learning_rate=0.2, decay_rate=0.01):
    '''
    Creates the multilayer network and trains the network

    Inputs:
        X - numpy.ndarray (n,m) of training data
        Y - numpy.ndarray (1,m) of training data labels
        net_dims - tuple of layer dimensions
        num_iterations - num of epochs to train
        learning_rate - step size for gradient descent

    Returns:
        costs - list of costs over training
        parameters - dictionary of trained network parameters
    '''
    parameters = initialize_multilayer_weights(net_dims)
    A0 = X
    costs = []
    costs_val = []
    for ii in range(num_iterations):
        ### CODE HERE
        # Forward Prop
        Z, cache = multi_layer_forward(A0, parameters)
        AL, cost = softmax_cross_entropy_loss(Z, Y)
        ## call to multi_layer_forward to get activations
        ## call to softmax cross entropy loss

        # Backward Prop
        dZl = softmax_cross_entropy_loss_der(AL, Y)
        gradients = multi_layer_backward(dZl, cache, parameters)
        parameters, alpha = update_parameters(parameters, gradients, ii, learning_rate, decay_rate)
        ## call to softmax cross entropy loss der
        ## call to multi_layer_backward to get gradients
        ## call to update the parameters
        # print(cost)

        if learning_rate > 5:
            Z, cache = multi_layer_forward(val_data, parameters)
            AL, cost_val = softmax_cross_entropy_loss(Z, val_label)
            costs.append(cost)
            costs_val.append(cost_val)
        elif ii % 10 == 0:
            Z, cache = multi_layer_forward(val_data, parameters)
            AL, cost_val = softmax_cross_entropy_loss(Z, val_label)
            costs.append(cost)
            costs_val.append(cost_val)
        if ii % 10 == 0:
            print("Cost at iteration %i is: %.05f, learning rate: %.05f" % (ii, cost, alpha))

    return costs, costs_val, parameters


def main():
    '''
    Trains a multilayer network for MNIST digit classification (all 10 digits)
    To create a network with 1 hidden layer of dimensions 800
    Run the progam as:
        python deepMultiClassNetwork_starter.py "[784,800]"
    The network will have the dimensions [784,800,10]
    784 is the input size of digit images (28pix x 28pix = 784)
    10 is the number of digits

    To create a network with 2 hidden layers of dimensions 800 and 500
    Run the progam as:
        python deepMultiClassNetwork_starter.py "[784,800,500]"
    The network will have the dimensions [784,800,500,10]
    784 is the input size of digit images (28pix x 28pix = 784)
    10 is the number of digits
    '''
    net_dims = ast.literal_eval(sys.argv[1])
    net_dims.append(10)  # Adding the digits layer with dimensionality = 10
    print("Network dimensions are:" + str(net_dims))

    # getting the subset dataset from MNIST
    data, label, test_data, test_label = \
        mnist(noTrSamples=6000, noTsSamples=1000,
              digit_range=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
              noTrPerClass=600, noTsPerClass=100)

    for i in range(10):
        if i == 0:
            train_data = data[:, :500]
            val_data = data[:, 500:600]
            train_label = label[:, :500]
            val_label = label[:, 500:600]
        else:
            train_data = np.concatenate([train_data, data[:, 600 * (i):(500 + (i) * 600)]], axis=1)
            val_data = np.concatenate([val_data, data[:, (500 + (i) * 600):(500 + (i) * 600) + 100]], axis=1)
            train_label = np.concatenate([train_label, label[:, 600 * (i):(500 + (i) * 600)]], axis=1)
            val_label = np.concatenate([val_label, label[:, (500 + (i) * 600):(500 + (i) * 600) + 100]], axis=1)
    # initialize learning rate and num_iterations
    learning_rate = 1.5
    num_iterations = 500


    cost_tr, cost_val, parameters = multi_layer_network(train_data, train_label, val_data, val_label, net_dims,
                                                        num_iterations=num_iterations, learning_rate=learning_rate)
    # compute the accuracy for training set and testing set
    train_Pred = classify(train_data, parameters)
    test_Pred = classify(test_data, parameters)

    trAcc = accuracy(train_Pred, train_label)
    teAcc = accuracy(test_Pred, test_label)
    print("Accuracy for training set is {0:0.3f} %".format(trAcc))
    print("Accuracy for testing set is {0:0.3f} %".format(teAcc))
    plt.xlabel("iterations")
    plt.ylabel("cost")
    plt.title("Multiclass - iterations vs cost for train and validation data")
    plt.plot(cost_tr, "-g", label='train')
    plt.plot(cost_val, ":b", label='val')
    plt.legend()
    plt.show()
    ### CODE HERE to plot costs


def accuracy(predictions, labels):
    correct_predictions = np.sum(predictions == labels)
    accuracy = 100.0 * correct_predictions / predictions.shape[0]
    return accuracy


if __name__ == "__main__":
    main()