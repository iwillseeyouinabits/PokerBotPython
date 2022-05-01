class GUI(object):


	def printHand(self, hand):
		print(hand)
		cardLines = []
		for card in hand:
			suit = card[0]
			rank = card[1]
			fRank = open('./CardText/' + str(rank) + '.txt', 'r')
			fSuit = open('./CardText/S' + str(suit) + '.txt', 'r')
			cardLines.append(fRank.readlines())
			cardLines.append(fSuit.readlines())
			fRank.close()
			fSuit.close()
		print()
		print()
		for i in range(12):
			for card in cardLines:
				print(card[i].replace('\n', '') , end =" ")
			print()
