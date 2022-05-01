import math


class Rank(object):

	def __init__(self, hand):
		self.hand = hand

	def isFlush(self):
		suits = [0]*4
		for card in self.hand:
			suits[card[0]] += 1
		for suit in suits:
			if suit == 5:
				maxInd = 0
				for card in self.hand:
					if card[0] == suit:
						maxInd = max(maxInd, card[1])
				return maxInd/13
		return -1

	def isStreight(self):
		rank = [0]*13
		for card in self.hand:
			rank[card[1]] += 1
		maxInd = -1
		for i in range(0, 13-5):
			streight = True
			for j in range(0, 5):
				if rank[i+j] == 0:
					streight = False
					break
			if streight:
				maxInd = max(maxInd, i+4)
		if maxInd < 0:
			return -1
		else:
			return maxInd/13

	def numOfKind(self):
		rank = [0]*13
		for card in self.hand:
			rank[card[1]] += 1
		for i in range(len(rank)):
			if rank[i] == max(rank):
				return (max(rank), i/13)

	def isTwoPair(self):
		rank = [0]*13
		for card in self.hand:
			rank[card[1]] += 1
		numPair = 0
		for r in rank:
			if r == 2:
				numPair += 1
		if not numPair == 2:
			return -1
		else:
			maxInd = 0
			for i in range(len(rank)):
				if rank[i] == max(rank):
					return i/13

	def isFullHouse(self):
		rank = [0]*13
		for card in self.hand:
			rank[card[1]] += 1
		has3 = False
		has2 = False
		for r in rank:
			if r == 3:
				has3 = True
			if r == 2:
				has2 = True
		if has2 and has3:
			for i in range(len(rank)):
				if rank[i] == 3:
					return i/13
		else:
			return -1



	def getRank(self, prnt = False):
		if self.isFlush() >= 0 and self.isStreight() >= 0:
			if prnt:
				print("streight flush")
			return 8 + self.isStreight()
		if self.numOfKind()[0] == 4:
			if prnt:
				print("Four Of Kind")
			return 7 + self.numOfKind()[1]
		if self.isFullHouse() >= 0:
			if prnt:
				print("Full House")
			return 6 + self.isFullHouse()
		if self.isFlush() >= 0:
			if prnt:
				print("flush")
			return 5 + self.isFlush()
		if self.isStreight() >= 0:
			if prnt:
				print("streight")
			return 4+self.isStreight()
		if self.numOfKind()[0] == 3:
			if prnt:
				print("Three of Kind")
			return 3 + self.numOfKind()[1]
		if self.isTwoPair() >= 0:
			if prnt:
				print("two pair")
			return 2 + self.isTwoPair()
		if self.numOfKind()[0] == 2:
			if prnt:
				print("pair")
			return 1 + self.numOfKind()[1]
		return 0
