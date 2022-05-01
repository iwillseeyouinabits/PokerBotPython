import math
import random

class Deck(object):

	def __init__(self):
		self.deck = []
		self.newDeck()

	def newDeck(self):
		self.deck = []
		for suit in range(0, 4):
			for rank in range(0, 13):
				self.deck.append((suit, rank))
		# random.shuffle(self.deck)

	def drawCard(self):
		index = random.randint(0, len(self.deck)-1)
		return self.deck.pop(index)

	def drawNCards(self, N):
		out = []
		for i in range(0, N):
			out.append(self.drawCard())
		return out

	def removeCard(self, card):
		self.deck.remove(card)
		return card
