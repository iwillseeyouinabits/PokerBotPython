from random import random
from sklearn.linear_model import LogisticRegression as LR
import json
import numpy as np

class LogisticRegression(object):

	def __init__(self, data):
		self.data = data
		self.model = LR()
		dataParsed = self.stripData(self.data)
		self.train(np.array(dataParsed[0]), np.array(dataParsed[1]))
	
	def stripData(self, data):
		inputs = []
		outputs = []
		for datum in data:
			inputs.append(datum[0])
			out = datum[1]
			outputs.append(out.index(max(out)))
		return (inputs, outputs)

	def fire(self, input):
		return  self.model.predict(input)

	def getWeights(self):
		return self.data
        
	def networkToFile(self, x):
		dataFile = open("brain" + str(x) + ".json", "w")
		dataFile.write(json.dumps(self.getWeights()))
		dataFile.close()
    
	def fileToNetwork(self, f):
		wFile = open(f, "r")
		return json.loads(wFile.read())
	
	def train(self, X, Y):
		print
		self.model.fit(X,Y)
