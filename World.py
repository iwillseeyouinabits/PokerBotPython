import NeuralNetwork
import Player
import random
import Game
import time
import copy
from threading import Thread

class World(object):


	def getPlayers(self, numInGen):
		nn = NeuralNetwork.NeuralNetwork([], [])
		players = []
		for i in range(numInGen):
			players.append([Player.Player(2000, "N"+str(i), nn.randomWeights(9, 15, 6, 1)), 0])
		return players

	def playGame(self, players, i, numHands):
		numHands = Game.Game(players[i][0], players[i+1][0]).playNGames(numHands, False)
		if players[i][0].getBankroll() > players[i+1][0].getBankroll() and numHands > 3 and (players[i][0].getFCR()[0][2] +  players[i][0].getFCR()[1][2] + players[i][0].getFCR()[2][2] + players[i][0].getFCR()[3][2]) > 5:
			players[i][1] += 1
		elif players[i][0].getBankroll() < players[i+1][0].getBankroll() and numHands > 3 and (players[i+1][0].getFCR()[0][2] +  players[i+1][0].getFCR()[1][2] + players[i+1][0].getFCR()[2][2] + players[i+1][0].getFCR()[3][2]) > 5:
			players[i+1][1] += 1

	def runComp(self, players, numGen, numHands):
		for gen in range(numGen):
			print()
			print()
			print("Game: " + str(gen))
			random.shuffle(players)
			threads = []
			print("start")
			for i in range(0, len(players), 2):
				threads.append(Thread(target=self.playGame, args=(players, i, numHands)))
			print("run")
			for thread in threads:
				thread.start()
			print("join")
			for thread in threads:
				thread.join()
			players.sort(key=lambda x:x[1])
			players = players[::-1]
			for player in players:
				print(player)
			print("fin")
			for p in players:
				p[0].reset(200)

	def makeNewGen(self, players):
		players.sort(key=lambda x:x[1])
		players = players[::-1]
		print()
		print()
		for player in players:
			print(player)
		#time.sleep(30)
		size = len(players)
		for i in range(size):
			w = players[i][0].getBrain()
			nn = NeuralNetwork.NeuralNetwork(w,[0]*9).networkToFile(i)
		players = players[:size//2]
		iter = 0
		playersTemp = copy.deepcopy(players)
		for player in playersTemp:
			print(iter)
			w = player[0].getBrain()
			for i in range(len(w)):
				for j in range(len(w[i])):
					for k in range(len(w[i][j])):
						if random.uniform(0,1) > 0.9:
							w[i][j][k] = 2*random.uniform(0,1)-1
			players.append([Player.Player(200, player[0].getName() + "_" + str(iter), w) , 0])
			iter += 1
		for i in range(len(players)):
			players[i][1] = 0
		return players

	def runGenetics(self, numPlayers, numGames, numHands, numGen):
		players = self.getPlayers(numPlayers)
		for gen in range(numGen):
			print("GENERATION ===> " + str(gen))
			self.runComp(players, numGames, numHands)
			players = self.makeNewGen(players)

