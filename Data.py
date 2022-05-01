import Deck
import Rank
import copy
import json

class Data(object):

	def getWinRate(self, pocket, share, N):
		deck = Deck.Deck()
		for card in pocket:
			deck.removeCard(card)
		for card in share:
			deck.removeCard(card)
		numWins = 0
		for i in range(N):
			deck2 = copy.deepcopy(deck)
			tempShare = share + deck2.drawNCards(5-len(share))
			pocket2 = deck2.drawNCards(2)
			if Rank.Rank(pocket + tempShare).getRank() >= Rank.Rank(pocket2 + tempShare).getRank():
				numWins += 1
		return numWins/N

	def getData(self, pocket, share, N, player, betToCall):
		out = player.getStats() + [self.getWinRate(pocket, share, N), (Rank.Rank(share).getRank()+1)/(Rank.Rank(pocket+share).getRank()+1), betToCall]
		if float("NAN") in out:
			print(out)
		return out

	def getFileData(self, fileName):
		lines = open(fileName, "r").readlines()
		data = []
		for i in range(0,len(lines), 2):
			din = json.loads(lines[i])
			dout = json.loads(lines[i+1])
			data.append([din, dout])
		return data