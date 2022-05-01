import math
import random
import time

import Rank
import Data
import GUI
import NeuralNetwork

class PlayerHuman(object):

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

	def makeBet(self, pot, minbet, hand, player2):
		print()
		print()
		print()
		print(GUI.GUI().printHand(hand))
		print("Pot ==> " + str(pot))
		print(self)
		print(player2)
		print("Choose:")
		print("fold: 0")
		print("Call " + str((pot-minbet)*(0/4)+minbet) + ": 1")
		print("Bet " + str((pot-minbet)*(1/4)+minbet) + ": 2")
		print("Bet " + str((pot-minbet)*(2/4)+minbet) + ": 3")
		print("Bet " + str((pot-minbet)*(3/4)+minbet) + ": 4")
		print("Bet " + str((pot-minbet)*(4/4)+minbet) + ": 5")
		try:
			maxInd = int(input())
		except:
			print("WRONG INPUT!!!")
			time.sleep(5)
			return self.makeBet(pot,minbet,hand,player2)

		bet = 0
		if maxInd == 0:
			bet = 0
		else:
			maxInd -= 1
			bet = (pot-minbet)*(maxInd/4)+minbet
		bet = self.filterBet(pot, minbet, int(bet), 10)
		self.bankroll -= bet
		return bet
