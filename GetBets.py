class GetBets(object):

	def __init__(self, player1, player2, hand1, hand2, pot):
		self.player1 = player1
		self.player2 = player2
		self.hand1 = hand1
		self.hand2 = hand2
		self.pot = pot
		
	def getNextBet(self, round, player, p2, pot, betToCall, hand, prnt):
		bet = player.makeBet(pot, betToCall, hand, p2)
		player.setLastBets(round, bet, pot)

		if bet < betToCall and not (bet == 0 and player.getBankroll() == 0):
			#folds
			if prnt:
				print(str(player) + " - Folds")
			player.modifyFCR(round, 0)
			p2.addToBankroll(pot)
			return (0, 0)
		elif bet > betToCall and not p2.getBankroll() == 0:
			#raise
			if prnt:
				print(str(player) + " - Raise " + str(bet))
			player.modifyFCR(round, 2)
			return (bet, 2)
		elif bet == betToCall or (bet == 0 and player.getBankroll() == 0):
			#call
			if prnt:
				print(str(player) + " - Call")
			player.modifyFCR(round, 1)
			return (bet, 1)
		elif p2.getBankroll() == 0:
			#call All In
			if prnt:
				print(str(player) + " - Calls All In")
			player.addToBankroll(bet)
			return (0, 1)
		
		
	def getBets2(self, round, prnt):
		betToCall = 0
		pot = self.pot
		for i in range(1000000000000000000000):
			flop = i%2 == 0
			p2 = None
			player = None
			hand = None
			if flop:
				p2 = self.player2
				player = self.player1
				hand = self.hand1
			else:
				player = self.player2
				p2 = self.player1
				hand = self.hand2
			
			play = self.getNextBet(round, player, p2, pot, betToCall, hand, prnt)
			bet = play[0]
			fcr = play[1]
			pot += bet
			if fcr == 1 and i > 0:
				return (pot, 1)
			elif fcr == 2:
				betToCall = bet - betToCall
			elif fcr == 0:
				return (pot, 0)
			
			
			
			
		
		
		
		
		
		
	def getBets(self, round, prnt):
		oldMinBet = 0
		sumP1 = 0
		sumP2 = 0
		for i in range(1000000000000):
			minBet = oldMinBet
			betP1 = self.player1.makeBet(self.pot, minBet-sumP1, self.hand1, self.player2)
			self.player1.setLastBets(round, betP1, sumP1+sumP2+self.pot)

			if betP1 < minBet-sumP1 and not (betP1 == 0 and self.player1.getBankroll() == 0):
				if prnt:
					print("P1 Folds")
				self.player1.modifyFCR(round, 0)
				self.player2.addToBankroll(self.pot)
				return 0
			elif betP1 > minBet-sumP1 and not self.player2.getBankroll() == 0:
				if prnt:
					print("P1 Raises " + str(betP1))
				self.player1.modifyFCR(round, 2)
				sumP1 += betP1
				minBet = sumP1
				self.pot += betP1
			elif betP1 == minBet-sumP1 or (betP1 == 0 and self.player1.getBankroll() == 0):
				if prnt:
					print("P1 Calls")
				self.player1.modifyFCR(round, 1)
				self.pot += betP1
			elif self.player2.getBankroll() == 0:
				self.player1.addToBankroll(betP1)
				if prnt:
					print("P1 Calls P2's All in")


			if minBet == oldMinBet and i > 0:
				return self.pot
			else:
				oldMinBet = minBet

			betP2 = self.player2.makeBet(self.pot, minBet-sumP2, self.hand2, self.player1)
			self.player2.setLastBets(round, betP2, sumP1+sumP2+self.pot)
			if betP2 < minBet-sumP2  and not (betP2 == 0 and self.player2.getBankroll() == 0):
				if prnt:
					print("P2 Folds")
				self.player2.modifyFCR(round, 0)
				self.player1.addToBankroll(self.pot)
				return 0
			elif betP2 > minBet-sumP2 and not self.player1.getBankroll() == 0:
				if prnt:
					print("P2 Raises " + str(betP2))
				self.player2.modifyFCR(round, 2)
				sumP2 += betP2
				minBet = sumP2
				self.pot += betP2
			elif betP2 == minBet-sumP2 or (betP2 == 0 and self.player2.getBankroll() == 0):
				if prnt:
					print("P2 Calls")
				self.player2.modifyFCR(round, 1)
				self.pot += betP2
			elif self.player1.getBankroll() == 0:
				self.player2.addToBankroll(betP2)
				if prnt:
					print("P2 Calls P1's All in")

			if minBet == oldMinBet:
				return self.pot
			else:
				oldMinBet = minBet
