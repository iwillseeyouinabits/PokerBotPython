import Neuron


class Layer(object):

    def __init__(self, inputs, weights, size):
        self.inputs = inputs
        self.weights = weights
        self.size = size
        self.neurons = []
        self.buildLayer()

    def buildLayer(self):
        for i in range(self.size):
            self.neurons.append(Neuron.Neuron(self.weights[i], self.inputs))

    def fire(self):
        out = []
        for i in range(self.size):
            out.append(self.neurons[i].fire())
        return out

    def getInputs(self):
        return self.inputs

    def getWeights(self):
        return self.weights

    def getSize(self):
        return self.size

    def getNeurons(self):
        return self.neurons
