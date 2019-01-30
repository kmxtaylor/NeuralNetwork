import os
import random
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches


class network():

    def __init__(self, layerSizes, learningRate):
        """
        This runs automatically to initialize the attributes for an instance of a class when the instance is created. It takes in list layerSizes that has the number of neurons per layer and uses it to determine the number of layers and randomize the NumPy arrays of weights and biases.
        """
        self.layerSizes = layerSizes
        self.learningRate = learningRate
        # lists in which each element is an array for each layer, which each contain the connections/neurons for that layer: weight for each connection (90) and a bias for each hidden and output neuron (10)

        allWList = []
        allBList = []

        for layer in range(len(layerSizes)-1):
            wInLayerList = []

            for receivingN in range(layerSizes[layer+1]):
                wForNeuronList = []

                for givingN in range(layerSizes[layer]):
                    wForNeuronList.append(random.uniform(-1, 1))

                wInLayerList.append(wForNeuronList)

            wInLayerArray = np.reshape(
                (np.asarray(wInLayerList)),
                (self.layerSizes[layer+1], self.layerSizes[layer])
            )
            allWList.append(wInLayerArray)

        self.w = allWList

        for layer in range(len(layerSizes)-1):
            bInLayerList = []

            for neuron in range(layerSizes[layer+1]):
                bInLayerList.append(random.uniform(-1, 1))

            bInLayerArray = np.reshape(
                (np.asarray(bInLayerList)),
                (self.layerSizes[layer+1], 1)
            )
            allBList.append(bInLayerArray)

        self.b = allBList

    def runNetwork(self):
        """
        This part of the program will prepare each minibatch's inputs to be fed through the network and serve as the base of the network to pass information between other functions in the network.
        """

        with open(
                r"ticTacToeData.csv", newline=''
        ) as dataFile:
            # non-subscriptable objects aren't containers & don't have indices
            minibatches = self.makeMinibatchesList(dataFile)
            minibatchNum = 1
            accuracyRates = []
            numCorrect = 0
            for minibatch in minibatches:
                tOut = minibatch[9]
                minibatchInputs = minibatch[0:9]  # end is exclusive
                inputs = np.reshape(
                    (np.asarray(minibatchInputs)),
                    (self.layerSizes[0], 1)
                )  # (rows, columns)
                expOut = self.feedforward(inputs)
                self.updateWB(expOut, inputs)

                # evaluate accuracy of predictions:
                expOut = round(expOut)
                if expOut == tOut:
                    numCorrect = numCorrect + 1

                groupsOf = 50
                if minibatchNum % groupsOf == 0:
                    percentsCorrect = float(
                        round((numCorrect/groupsOf)*100)
                    )
                    accuracyRates.append(percentsCorrect)
                    numCorrect = 0
                minibatchNum = minibatchNum + 1
            print(f"Accuracy rates in groups of {groupsOf}: {accuracyRates}")
            return accuracyRates

    def makeMinibatchesList(self, dataFile):
        """
        Convert csv file of characters to a list of lists of floats for each minibatch (line).
        """
        minibatches = []
        for minibatch in dataFile:  # each row begins as string
            minibatchSplit = minibatch.strip().split(",")
            for i in range(len(minibatchSplit)-1):
                if minibatchSplit[i] == "x":
                    minibatchSplit[i] = 1.0
                else:  # o or b
                    minibatchSplit[i] = 0.0

            if minibatchSplit[9] == 'positive':  # theoretical output
                    minibatchSplit[9] = 1.0
            elif minibatchSplit[9] == 'negative':
                minibatchSplit[9] == 0.0
            minibatches.append(minibatchSplit)
        return minibatches

    def feedforward(self, inputs):
        """
        Return the output of the network for an array of network inputs.
        """
        for bArray, wArray in zip(self.b, self.w):  # layers/arrays = 2
            activation = self.sigmoid(np.dot(wArray, inputs)+bArray)
            inputs = activation
            # 1st iteration returns an array of 9 single element lists
        expOut = activation[0][0]
        return expOut

    def sigmoid(self, dotProdSum):
        """
        The sigmoid activation function put the inputs, weights, and biases into a function that helps us determine the output array of the layer.
        """
        activation = 1/(1+np.exp(-dotProdSum))
        return activation

    def updateWB(self, expOut, inputs):
        """
        Updates the weights and biases of the network based on the partial derivatives of the cost function. Variables are self (class specific variable), the list miniBatch, and the learning rate.
        """

        nablaW = [np.zeros(layer.shape) for layer in self.w]
        # print(nablaW)
        nablaB = [np.zeros(layer.shape) for layer in self.b]
        # print(nablaB)

        deltaNablaB, deltaNablaW = self.backprop(
            expOut, inputs)

        nablaW = [nablaW + deltaNablaW for nablaW,
                  deltaNablaW in zip(nablaW, deltaNablaW)]

        nablaB = [nablaB + deltaNablaB for nablaB,
                  deltaNablaB in zip(nablaB, deltaNablaB)]

        self.w = [w - (self.learningRate/(self.layerSizes[0]+1)) *
                  nablaW for w, nablaW in zip(self.w, nablaW)]

        self.b = [b - (self.learningRate/(self.layerSizes[0]+1)) *
                  nablaB for b, nablaB in zip(self.b, nablaB)]

    def backprop(self, expOut, inputs):
        """
        Uses feedforward of network to calculate error for output layer, uses that to backpropagate error to other layers, and finally find the change in weights and biases based on the errors
        """
        nablaW = [np.zeros(layer.shape) for layer in self.w]
        # print(nablaW)
        nablaB = [np.zeros(layer.shape) for layer in self.b]
        # print(nablaB)
        activation = inputs
        activations = [inputs]
        weightedSumList = []
        # feedforward
        for bArray, wArray in zip(self.b, self.w):  # layers/arrays = 2
            weightedSum = np.dot(wArray, inputs)+bArray
            weightedSumList.append(weightedSum)
            # print(weightedSumList)
            activation = self.sigmoid(weightedSum)
            activations.append(activation)
        		# print(activations)

        # error and output change calculations
        error = self.costDerivative(
                activations[-1], expOut) * self.sigmoidPrime(weightedSumList[-1])
        nablaB[-1] = error
        nablaW[-1] = np.dot(error, activations[-2].transpose())

        # backpropagate error using output error
        # find change in weights and biases for entire network
        for L in range(2, len(self.layerSizes)):
            weightedSum = weightedSumList[-L]
            sp = self.sigmoidPrime(weightedSum)
            error = np.dot(self.w[-L+1].transpose(), error) * sp
            # print(nablaB[-L])
            nablaB[-L] = error
            # print(f"nablaB array for layer {-L}: {nablaB[-L]}")
            nablaW[-L] = np.dot(error, activations[-L-1].transpose())
            # print(f"nablaW array for layer {-L}: {nablaW[-L]}")
        return nablaB, nablaW

    def sigmoidPrime(self, s):
        """
        Function for the derivative of the activation function. Used to find the error of each neuron
        """
        return self.sigmoid(s)*(1-self.sigmoid(s))

    def costDerivative(self, expOut, tOut):
        """
        Function for the derivative of the cost function. Used to find the error of each neuron
        """
        networkOut = np.array(expOut, dtype='float64')
        y = np.array(tOut, dtype='float64')
        costPrime = np.subtract(networkOut, y)
        return costPrime


def main():
    """
    This function sets the sizes of the layers and the learning rate of the network.
    """
    # inputNuerons = int(input("How many inputs do you have? \n"))
    inputNuerons = 9  # debugging
    # outputNuerons = int(input("How many outputs do you want? \n"))
    outputNuerons = 1  # debugging
    neuronsPerLayer = [inputNuerons, inputNuerons, outputNuerons]
    # learningRate = float(input("What's the learning rate \n"))
    learningRate = 1  # debugging
    network1 = network(neuronsPerLayer, learningRate)
    return network1.runNetwork()


def graphUpdate(frame):
    # frames are for some reason starting at 1 and counting up by 2
    xdata.append(frame)
    ydata.append(percentagesCorrect[int(frame)])
    # Set the x and y data; ACCEPTS: 2D array (rows are x, y) or two 1D arrays
    graphLine.set_data(xdata, ydata)
    return graphLine,


if __name__ == "__main__":

    percentagesCorrect = main()
    numIterations = len(percentagesCorrect)

    plt.switch_backend('TkAgg')

    # initialize graph:
    fig, ax = plt.subplots()
    graphLine, = plt.plot([], [], 'r-', animated=True)
    redPatch = mpatches.Patch(color='red',label='Network')
    plt.legend(handles=[redPatch], loc="upper right")
    plt.xlabel("Iterations")
    plt.ylabel("Percentage Correct")
    plt.title("Percentage Correct Over Time")
    plt.axis([1, numIterations, 0, 100])  # ([x start, x end, y start, y end])

    ticksList = []
    for i in range(1, numIterations):
        ticksList.append(i)
    ax.set_xticks(ticksList)

    xdata, ydata = [], []
    ani = animation.FuncAnimation(fig,
                                  graphUpdate,
                                  frames=np.linspace(
                                    1,
                                    numIterations,
                                    num=numIterations
                                    ),
                                    blit=True
    )
    plt.show()