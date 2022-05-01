import Deck
import GetBets
import Rank
import time

class Game(object):


	def __init__(self, player1, player2):
		self.player1 = player1
		self.player2 = player2

	def playGame(self, flip, blinds, prnt):
		self.player1.addNumGames()
		self.player2.addNumGames()
		deck = Deck.Deck()
		round = 0
		pot = 0
		if flip:
			pot += self.player1.takeFromBankroll(blinds)
			pot += self.player2.takeFromBankroll(2 * blinds)
		else:
			pot += self.player1.takeFromBankroll(2 * blinds)
			pot += self.player2.takeFromBankroll(blinds)
		pocket1 = deck.drawNCards(2)
		pocket2 = deck.drawNCards(2)
		self.player1.resetLastBets()
		self.player2.resetLastBets()
		share = []
		for round in range(4):
			if prnt:
				print("Round " + str(round))
			if round == 1:
				share += deck.drawNCards(3)
			elif round > 1:
				share += [deck.drawCard()]
			getBets = None
			if flip:
				getBets = GetBets.GetBets(self.player1, self.player2, pocket1+share, pocket2+share, pot).getBets2(round, prnt)
			else:
				getBets = GetBets.GetBets(self.player2, self.player1, pocket2+share, pocket1+share, pot).getBets2(round, prnt)
			if getBets[1] == 0:
				return (pocket1 + share, pocket2 + share)
			pot = getBets[0]

		rankP1 = Rank.Rank(pocket1 + share).getRank()
		rankP2 = Rank.Rank(pocket2 + share).getRank()
		if rankP1 == rankP2:
			if prnt:
				print("Tie")
			self.player1.addToBankroll(pot//2)
			self.player2.addToBankroll(pot//2)
		elif rankP1 > rankP2:
			if prnt:
				print("Player 1 Wins")
			self.player1.addToBankroll(pot)
		else:
			if prnt:
				print("Player 2 Wins")
			self.player2.addToBankroll(pot)
		return (pocket1 + share, pocket2 + share)


	def playNGames(self, N, prnt):
		for i in range(N):
			if prnt:
				print()
				print("Game__________________: " + str(i))
				print()
			self.playGame(i%2==0, 10, prnt)
			if self.player1.getBankroll() <= 0 or self.player2.getBankroll() <= 0:
				return i
		return 0
