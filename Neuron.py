import math


class Neuron(object):

    def __init__(self, weights, inputs):
        self.weights = weights
        self.inputs = inputs
        self.total = 0
        self.bias = 1
        self.setTotal()

    def setTotal(self):
        for i in range(len(self.weights)):
            self.total += self.weights[i] * self.inputs[i]
        self.total += self.bias

    def fire(self):
        return self.squash(self.total)

    @staticmethod
    def squash(total):
        return 1.0 / (1.0 + (math.exp(-total)))

    def getInputs(self):
        return self.inputs

    def getWeights(self):
        return self.weights

    def getTotal(self):
        return self.total
