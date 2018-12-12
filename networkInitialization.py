import os
import random
import numpy as np
import math

# asks user to set number of layers and neurons and outputs (9,9,1)
# randomizes weights and biases
# x = 1 and b,o = 0
# setting minibatch (row) that runs through each time and changes weights and biases based on accuracy


class network():

    def __init__(self, layerSizes):
        """
        This runs automatically to initialize the attributes for an instance of a class when the instance is created. It takes in list layerSizes that has the number of neurons per layer and uses it to determine the number of layers and randomize the NumPy arrays of weights and biases.
        """
        self.numLayers = len(layerSizes)
        self.layerSizes = layerSizes
        # lists in which each element is an array for each layer, which each contain the connections/neurons for that layer: weight for each connection (90) and a bias for each hidden and output neuron (10)
        self.w = [np.random.rand(y, x)
                  for x, y in zip(layerSizes[:-1], layerSizes[1:])]
        self.b = [np.random.rand(y, 1) for y in layerSizes[1:]]

    def inputMinibatch(self):
        """
        Reads csv file with data line by line (each line is a minibatch), converts input "x"s to 1 and "o"s and "b"s to 0, converts the line of data into two tuples of single item strings: the inputs and the theoretical output, and feeds forward each minibatch's inputs into the network.
        """
        with open("ticTacToeData.csv", "r", newline='') as dataFile:
            # non-subscriptable objects aren't containers and don't have indices
            for minibatch in dataFile:  # each row begins as string
                minibatch = dataFile.readline()  # need to iterate over all lines
                # print(f'minibatch: {minibatch}')  # debugging
                minibatchSplit = minibatch.split(",")  # split string into list
                minibatchInputs = minibatchSplit[0:9]  # end is exclusive
                theoreticalOutput = tuple(minibatchSplit[9])
                for i in range(len(minibatchInputs)):
                    if minibatchInputs[i] == "x":
                        minibatchInputs[i] = 1.0
                    else:  # if o or b
                        minibatchInputs[i] = 0.0
                inputs = np.reshape(
                    (np.asarray(minibatchInputs)),
                    (self.layerSizes[0], 1)
                )  # (rows, columns)
                expOutput = self.feedforward(inputs)
                print(expOutput)

    def feedforward(self, inList):
        """Return the output of the network if the inList of inputs is received."""
        for bArray, wArray in zip(self.b, self.w):  # layers/arrays = 2
            rawOut = self.sigmoid(np.dot(wArray, inList)+bArray)
            inList = rawOut  # my addition to account for the 2 layer spaces
            # 1st iteration returns an array of 9 single element lists
            # break
        expOut = round(rawOut[0][0])
        if expOut == 0.0:
            expOut = "negative"
        elif expOut == 1.0:
            expOut = "positive"
        return expOut

    def sigmoid(self, dotProdSum):
        """
        The sigmoid activation function put the inputs, weights, and biases into a function that helps us determine if the neuron fires or not.
        """
        sigOutput = 1/(1+(math.e**((-1)*dotProdSum)))
        return sigOutput


def main():
    # inputNuerons = int(input("How many inputs do you have? \n"))
    inputNuerons = 9  # debugging
    # outputNuerons = int(input("How many outputs do you want? \n"))
    outputNuerons = 1  # debugging
    neuronsPerLayer = [inputNuerons, inputNuerons, outputNuerons]
    # not sure how to call init() in network class
    network1 = network(neuronsPerLayer)
    network1.inputMinibatch()


if __name__ == main():
    import doctest
    doctest.testmod()
    main()
