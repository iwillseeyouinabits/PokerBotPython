import math
import random
import time

import NeuralNetwork


class Learn(object):

	def __init__(self, learningRate, resetIter):
		self.errorNeurons = [None]
		self.learningRate = learningRate
		self.errornum = 0
		self.errorden = 0
		self.resetIter = resetIter
		self.data = {}

	def learn(self, weights, inputs, rightOut):
		print("Inputs: " + str(inputs))
		out = NeuralNetwork.NeuralNetwork(weights, inputs).fire()
		for i in range(len(out)):
			print(str(out[i]) + " " + str(rightOut[i]) + " | ", end=" ")
		print()
		self.errorNeurons = [None]*len(weights)
		for x in range(len(weights) - 1, 0, -1):
			self.errorNeurons[x] = ([None] * len(weights[x]))
			for y in range(len(weights[x])):
				if x == len(weights) - 1:
					self.errorNeurons[x][y] = (out[y] - rightOut[y]) * self.derivative(
					NeuralNetwork.NeuralNetwork(weights, inputs).getLayers()[x].getNeurons()[y].getTotal())
					if not rightOut[out.index(max(out))] == 1:
						self.errornum +=1
					self.errorden += 1
					# self.errornum += abs(out[y] - rightOut[y])
					# self.errorden += abs(rightOut[y])
				else:
					self.errorNeurons[x][y] = 0
					for i in range(len(self.errorNeurons[x + 1])):
						self.errorNeurons[x][y] = self.errorNeurons[x + 1][i] * weights[x + 1][i][y]
					self.errorNeurons[x][y] *= self.derivative(
						NeuralNetwork.NeuralNetwork(weights, inputs).getLayers()[x].getNeurons()[y].getTotal())

				if x != 0:
					for z in range(len(weights[x][y])):
						weights[x][y][z] -= self.learningRate * self.errorNeurons[x][y] * NeuralNetwork.NeuralNetwork(weights, inputs).getLayers()[x - 1].getNeurons()[z].fire()
				else:
					for z in range(len(weights[x][y])):
						weights[x][y][z] -= self.learningRate * self.errorNeurons[x][y] * inputs[z]
		if self.errorden > 0:
			print(str(self.errornum / self.errorden) + "!!!!!!!!!!!!!!")
		return weights

	def learnRecur(self, numRuns, stopRate, weights, data):
		prog = 1000000.0
		i = 0
		self.setData(data)
		while i < (numRuns):
			print(i)
			if self.errorden > 0 and i > 800 and self.errornum/self.errorden <= stopRate:
				return weights
			if i % self.resetIter == 0 and self.errorden > 0 and self.errornum/self.errorden > prog:
				i = 0
				weights = NeuralNetwork.NeuralNetwork(weights, [1]*len(data[0][0])).resetWeights()
				self.errornum = 0
				self.errorden = 0
				prog = 1000000.0
				print("reset weights")
				time.sleep(5)
			elif i % self.resetIter == 0 and self.errorden > 0 and self.errornum/self.errorden < prog:
				prog = self.errornum/self.errorden
			datum = self.testData()
			weights = self.learn(weights, datum[0], datum[1])
			i+=1
		return weights

	@staticmethod
	def derivative(x):
		return (math.exp(x)) / math.pow((1.0 + math.exp(x)),2.0)

	def setData(self, data):
		for datum in data:
			inputs = []
			if tuple(datum[1]) in self.data:
				inputs = self.data[tuple(datum[1])]
			inputs.append(datum[0])
			self.data[tuple(datum[1])] = inputs

	def testData(self):
		while True:
			randHot = random.randint(0, 5)
			outputs = [0]*6
			outputs[randHot] = 1
			if tuple(outputs) in self.data:
				inputs = self.data[tuple(outputs)]
				if len(inputs) > 0:
					return [inputs[random.randint(0, len(inputs)-1)], outputs]