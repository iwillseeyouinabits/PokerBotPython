from random import random

import json
import Layer


class NeuralNetwork(object):

    def __init__(self, weights, inputs):
        self.weights = weights
        self.inputs = inputs
        self.size = len(self.weights)
        self.layers = []
        if len(weights) > 0:
            self.buildNetwork()

    def buildNetwork(self):
        for i in range(self.size):
            if i == 0:
                self.layers.append(Layer.Layer(self.inputs, self.weights[i], len(self.weights[i])))
            else:
                self.layers.append(Layer.Layer(self.layers[i - 1].fire(), self.weights[i], len(self.weights[i])))

    def fire(self):
        return self.layers[self.size - 1].fire()

    def getInputs(self):
        return self.inputs

    def getWeights(self):
        return self.weights

    def getSize(self):
        return self.size

    def getLayers(self):
        return self.layers

    def randomWeights(self, numInput, numNeuronsInHiddenLayer, numNeuronsInOutput, numHiddenLayers):
        self.weights = []
        for x in range(numHiddenLayers + 1):
            yMax = 0
            self.weights.append([])

            if x == numHiddenLayers:
                yMax = numNeuronsInOutput
            else:
                yMax = numNeuronsInHiddenLayer
            for y in range(yMax):
                zMax = 0
                self.weights[x].append([])

                if x == 0:
                    zMax = numInput
                else:
                    zMax = numNeuronsInHiddenLayer
                for z in range(zMax):
                    self.weights[x][y].append(2 * (random() - .5))
        self.size = len(self.weights)
        return self.weights
        
        

    def resetWeights(self):
        for x in range(len(self.weights)):
            for y in range(len(self.weights[x])):
                for z in range(len(self.weights[x][y])):
                    self.weights[x][y][z] = (2 * (random() - .5))
        return self.weights
        
        
        
    def networkToFile(self, x):
        dataFile = open("brain" + str(x) + ".json", "w")
        dataFile.write(json.dumps(self.weights))
        dataFile.close()
    
    def fileToNetwork(self, f):
        wFile = open(f, "r")
        return json.loads(wFile.read())
