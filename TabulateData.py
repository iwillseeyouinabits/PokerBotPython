
import matplotlib.pyplot as plt
import NeuralNetwork
import Player
import PlayerHuman
import Game

class TabulateData(object):



        def tabulateData1(self, maxInd, playNum, plotName, dataFileName):
                rates = []
                file = open(dataFileName, 'w')
                for k in range(1, maxInd, 2):
                        human = False
                        badBot = True
                        numGames = 50
                        nn = NeuralNetwork.NeuralNetwork([], [])
                        subrates = []
                        for r in range(5):
                                winCount = 0
                                for i in range(1,numGames):
                                        nn = NeuralNetwork.NeuralNetwork([], [])
                                        player1 = None
                                        if human:
                                                player1 = PlayerHuman.PlayerHuman(2000, "You", nn.randomWeights(9, 15, 6, 1))
                                        elif badBot:
                                                player1 = Player.Player(2000, "BadBot", nn.fileToNetwork("brain" + str(k-1) + "_" + str(r) + ".json"))
                                        else:
                                                player1 = Player.Player(2000, "Random Bot", nn.randomWeights(9, 15, 6, 1))
                                        player2 = Player.Player(2000, "Bot", nn.fileToNetwork("brain" + str(k) + "_" + str(playNum) + ".json"))
                                        Game.Game(player2, player1).playNGames(100, False)
                                        if player2.getBankroll() >= player1.getBankroll():
                                                winCount += 1
                                subrates.append((2*(winCount/(numGames-1)))-1)
                                print(subrates)
                        rates.append(sum(subrates)/len(subrates))
                        plt.bar(list(range(len(rates))), rates)
                        plt.savefig(plotName)
                        plt.close()
                file.write(str(rates))
                file.close()

        def tabulateData2(self, maxInd, playNum, plotName, dataFileName):
                rates = []
                file = open(dataFileName, 'w')
                for k in range(1, maxInd, 2):
                        human = False
                        badBot = True
                        numGames = 20
                        nn = NeuralNetwork.NeuralNetwork([], [])
                        subrates = []
                        for r in range(5):
                                winCount = 0
                                for i in range(1,numGames):
                                        nn = NeuralNetwork.NeuralNetwork([], [])
                                        player1 = None
                                        if human:
                                                player1 = PlayerHuman.PlayerHuman(2000, "You", nn.randomWeights(9, 15, 6, 1))
                                        elif badBot:
                                                player1 = Player.Player(2000, "BadBot", nn.fileToNetwork("brain" + str(k-1) + "_" + str(r) + ".json"))
                                        else:
                                                player1 = Player.Player(2000, "Random Bot", nn.randomWeights(9, 15, 6, 1))
                                        player2 = Player.Player(2000, "Bot", nn.fileToNetwork("brain" + str(maxInd-1) + "_" + str(playNum) + ".json"))
                                        Game.Game(player2, player1).playNGames(100, False)
                                        if player2.getBankroll() >= player1.getBankroll():
                                                winCount += 1
                                subrates.append((2*(winCount/(numGames-1)))-1)
                                print(subrates)
                        rates.append(sum(subrates)/len(subrates))
                        plt.bar(list(range(len(rates))), rates)
                        plt.savefig(plotName)
                        plt.close()
                file.write(str(rates))
                file.close()
