import math
import random
import Rank
import Data
import NeuralNetwork
import LogisticRegression
import SVM

class Player(object):

	def __init__(self, bankroll, name, w):
		self.bankroll = bankroll
		self.name = name
		self.w = w
		self.fcr = [[1,1,1], [1,1,1], [1,1,1], [1,1,1]]
		self.numGames = 0
		self.lastBets = [0, 0, 0, 0]

	def reset(self, bankroll):
		self.bankroll = bankroll
		self.fcr = [[1,1,1], [1,1,1], [1,1,1], [1,1,1]]
		self.numGames = 0

	def resetLastBets(self):
		self.lastBets = [0, 0, 0, 0]

	def setLastBets(self, round, amount, pot):
		self.lastBets[round] = amount/pot

	def getBrain(self):
		return self.w

	def getFoldRate(self):
		return (self.fcr[0][0] + self.fcr[1][0] + self.fcr[2][0] + self.fcr[3][0])/self.numGames

	def addToBankroll(self, win):
		self.bankroll += win

	def takeFromBankroll(self, take):
		self.bankroll -= take
		if self.bankroll >= 0:
			return take
		else:
			dif = self.bankroll
			self.bankroll = 0
			return take + dif

	def getVPIP(self):
		return (self.fcr[0][1] + self.fcr[0][2])/self.numGames

	def getPFR(self):
		return (self.fcr[0][2])/self.numGames

	def getAF(self):
		r = 0
		c = 0
		for fcr in self.fcr:
			r += fcr[2]
			c += fcr[1]
		return r/c

	def getFVPIP(self):
		return (self.fcr[1][1] + self.fcr[1][2])/self.numGames

	def getFR(self):
		return (self.fcr[1][2])/self.numGames


	def getTVPIP(self):
		return (self.fcr[2][1] + self.fcr[2][2])/self.numGames

	def getTR(self):
		return (self.fcr[2][2])/self.numGames


	def getRVPIP(self):
		return (self.fcr[3][1] + self.fcr[3][2])/self.numGames

	def getRR(self):
		return (self.fcr[3][2])/self.numGames

	def getStats(self):
		return [self.getAF(), self.getFoldRate()] + self.lastBets

	def addNumGames(self):
		self.numGames += 1

	def modifyFCR(self, round, fcr):
		self.fcr[round][fcr] += 1

	def getFCR(self):
		return self.fcr

	def getBankroll(self):
		return self.bankroll

	def getName(self):
		return self.name

	def __str__(self):
		return  self.name + ": " + str(self.bankroll)

	def __repr__(self):
		return  self.name + ": " + str(self.bankroll)

	def getBetOptions(self, pot, minbet):
		bets = [0]
		for i in range(5):
			bets.append((pot - minbet) * (i / 4) + minbet)
		for i in range(len(bets)):
			bets[i] = self.filterBet(pot, minbet, int(bets[i]), 10)
		return bets

	def filterBet(self, pot, minbet, bet, minraise):
		if bet > pot and bet <= self.bankroll and bet >= minbet+minraise:
			return pot
		elif bet <= pot and bet <= self.bankroll and bet >= minbet+minraise:
			return bet
		elif bet <= pot and bet <= self.bankroll and bet < minbet+minraise and bet >= minbet:
			return minbet
		elif bet > self.bankroll and self.bankroll <= pot:
			return self.bankroll
		else:
			return 0

	def getInputs(self, hand, player2, minbet, pot):
		return Data.Data().getData(hand[:2], hand[2:], 100, player2, minbet/pot)

	def makeBet(self, pot, minbet, hand, player2, betIn=None):
		inputs = self.getInputs(hand, player2, minbet, pot)
		maxInd = 0
		if "LR" in self.getName():
			maxInd = LogisticRegression.LogisticRegression(self.w).fire([inputs])[0]
		elif "SVM" in self.getName():
			maxInd = SVM.SVM(self.w).fire([inputs])[0]
		elif "NN" in self.getName():
			outputs = NeuralNetwork.NeuralNetwork(self.w, inputs).fire()
			maxInd = outputs.index(max(outputs))
		else:
			raise "Not a valid player"
		if maxInd == 0:
			bet = 0
		else:
			maxInd -= 1
			bet = (pot-minbet)*(maxInd/4)+minbet
		if not betIn == None:
			bet = betIn
		bet = self.filterBet(pot, minbet, int(bet), 10)
		self.bankroll -= bet
		return bet
