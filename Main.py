import matplotlib.pyplot as plt
import pandas as pd
import Learn
import NeuralNetwork
import json
import Learn
import Deck
import Rank
import Player
import PlayerHuman
import GetBets
import Game
import Data
import World
import UnitPoker
import TrainTwoNetworks
import TabulateData

class Main(object):

	def main(self):

		#TrainTwoNetworks.TrainTwoNetworks().train()

		TabulateData.TabulateData().tabulateData1(20, 0, "figV1_0.png", "dataFileV1_0.txt")
		TabulateData.TabulateData().tabulateData1(20, 1, "figV1_1.png", "dataFileV1_1.txt")
		TabulateData.TabulateData().tabulateData1(20, 2, "figV1_2.png", "dataFileV1_2.txt")
		TabulateData.TabulateData().tabulateData1(20, 3, "figV1_3.png", "dataFileV1_3.txt")
		TabulateData.TabulateData().tabulateData1(20, 4, "figV1_4.png", "dataFileV1_4.txt")


		# human = False
		# badBot = False
		# numGames = 200
		# winCount = 0
		# nn = NeuralNetwork.NeuralNetwork([], [])
		#
		# for i in range(numGames):
		# 	nn = NeuralNetwork.NeuralNetwork([], [])
		# 	player1 = None
		# 	if human:
		# 		player1 = PlayerHuman.PlayerHuman(2000, "You", nn.randomWeights(9, 15, 6, 1))
		# 	elif badBot:
		# 		player1 = Player.Player(2000, "BadBot", nn.fileToNetwork("brain99.json"))
		# 	else:
		# 		player1 = Player.Player(2000, "Random Bot", nn.randomWeights(9, 15, 6, 1))
		# 	player2 = Player.Player(2000, "Bot", nn.fileToNetwork("brain19_1.json"))
		# 	Game.Game(player2, player1).playNGames(100, True)
		# 	print(player1)
		# 	print(player2)
		# 	if player2.getBankroll() >= player1.getBankroll():
		# 		winCount += 1
		# print("Win Rate: " + str(winCount/numGames))

if __name__ == '__main__':
	Main().main()
