import random
import time

import Deck
import Rank
import Player
import copy

class UnitPoker(object):

    def getNextBet(self, round, player, p2, pot, betToCall, hand, prnt, raiseItr, bet = None):
        bet = player.makeBet(pot, betToCall, hand, p2, bet)
        player.setLastBets(round, bet, pot)

        if (bet < betToCall and not p2.getBankroll() == 0):
            # folds
            # print("raiseItr 2 " + str(raiseItr))
            if prnt:
                print(str(player) + " - Folds")
            player.modifyFCR(round, 0)
            p2.addToBankroll(pot)
            return (0, 0)
        elif bet > betToCall and not p2.getBankroll() == 0:
            # raise
            if prnt:
                print(str(player) + " - Raise " + str(bet))
            player.modifyFCR(round, 2)
            return (bet, 2)
        elif bet == betToCall or (bet == 0 and player.getBankroll() == 0):
            # call
            if prnt:
                print(str(player) + " - Call")
            player.modifyFCR(round, 1)
            return (bet, 1)
        elif p2.getBankroll() == 0:
            # call All In
            if prnt:
                print(str(player) + " - Calls All In")
            player.addToBankroll(bet)
            return (0, 1)
        else:
            print("Money On Table")

    def findWinner(self, p1, p2, hand1, hand2, share, pot, prnt = True):
        rankP1 = Rank.Rank(hand1 + share).getRank()
        rankP2 = Rank.Rank(hand2 + share).getRank()
        if rankP1 == rankP2:
            if prnt:
                print("Tie")
            p1.addToBankroll(pot // 2)
            p2.addToBankroll(pot // 2)
        elif rankP1 > rankP2:
            if prnt:
                print("Player 1 Wins")
            p1.addToBankroll(pot)
        else:
            if prnt:
                print("Player 2 Wins")
            p2.addToBankroll(pot)

    def startGame(self, p1, p2):
        p1.addNumGames()
        p2.addNumGames()
        p1.takeFromBankroll(10)
        p2.takeFromBankroll(10)
        p1.resetLastBets()
        p2.resetLastBets()

    def dealCards(self, deck, round):
        if round == 0:
            return deck.drawNCards(3)
        elif round > 0:
            return deck.drawNCards(1)

    def nextUnit(self, p1, p2, share, hand1, hand2, deck, pot, minbet, callable, flip, round, raisItr):
       plays = []
       if flip and random.random() > (0.8) + raisItr*0.07:
           plays = p1.getBetOptions(pot, minbet)
       elif flip:
           plays = [self.getNextBet(round, p1, p2, pot, minbet, share + hand1, False, raisItr)]
       else:
           # print("raiseItr " + str(raisItr))
           plays = [self.getNextBet(round, p2, p1, pot, minbet, share + hand2, False, raisItr)]


       moves = []
       oldp1 = copy.deepcopy(p1)
       oldp2 = copy.deepcopy(p2)
       oldpot = copy.deepcopy(pot)
       oldminbet = copy.deepcopy(minbet)
       oldraisitr = copy.deepcopy(raisItr)
       for play in plays:
           p1 = copy.deepcopy(oldp1)
           p2 = copy.deepcopy(oldp2)
           pot = copy.deepcopy(oldpot)
           minbet = copy.deepcopy(oldminbet)
           raisItr = copy.deepcopy(oldraisitr)

           dealCards = False

           if len(plays) > 1:
               play = self.getNextBet(round, p1, p2, pot, minbet, share + hand1, False, raisItr, play)
           bet = play[0]
           fcr = play[1]
           pot += bet
           cont = True

           if fcr == 2:
               raisItr += 1
           else:
               raisItr = 0

           if fcr == 0:
               callable = False
               cont = False
           elif fcr == 1 and not callable:
               callable = True
           elif fcr == 1 and callable and round < 3:
               callable = False
               # share += self.dealCards(deck, round)
               dealCards = True
               round += 1
               # print("Round => " + str(round))
               minbet = 0
           elif fcr == 1 and callable and round == 3:
               cont = False
               callable = False
               self.findWinner(p1, p2, hand1, hand2, share, pot, False)
           elif fcr == 2:
               callable = True
               minbet = bet - minbet
           else:
               raise Exception("Wrong Move Made")

           if cont:
               if not dealCards:
                   moves.append(self.nextUnit(*(copy.deepcopy(p1), copy.deepcopy(p2), copy.deepcopy(share), copy.deepcopy(hand1), copy.deepcopy(hand2), copy.deepcopy(deck), pot, minbet, callable, not flip, round, raisItr)))
               else:
                   numDeal = 5
                   subMoves = []
                   for i in range(numDeal):
                       tempDeck = copy.deepcopy(deck)
                       tempShare = share + self.dealCards(tempDeck, round-1)
                       subMoves.append(self.nextUnit(*(copy.deepcopy(p1), copy.deepcopy(p2), copy.deepcopy(tempShare), copy.deepcopy(hand1), copy.deepcopy(hand2), tempDeck, pot, minbet, callable, not flip, round, raisItr)))
                   subMoves = sorted(subMoves,key=lambda x: x[0])
                   mov = (subMoves[numDeal//2 + 1][0], subMoves[numDeal//2 + 1][1], subMoves[numDeal//2 + 1][2])
                   # print(subMoves)
                   moves.append(mov)
           else:
               moves.append((p1.getBankroll(), copy.deepcopy(p1), copy.deepcopy(p2)))
       maxInd = 0
       maxBank = 0
       for i in range(len(moves)):
           if moves[i][0] >= maxBank:
               maxBank = moves[i][0]
               maxInd = i
       if len(moves) > 1:
           out = [0]*6
           out[maxInd] = 1
           input = p1.getInputs(hand1 + share, p2, minbet, pot)
           file = open("data.txt", "a")
           file.write(str(input) + "\n")
           file.write(str(out) + "\n")
           file.close()

       # print(str(moves) + " " + str(pot) + " " + str(round))
       # print(moves[maxInd])
       return moves[maxInd]

    def playHand(self, p1, p2, flip):
       p1.addNumGames()
       p2.addNumGames()
       deck = Deck.Deck()
       round = 0
       pot = 0
       if flip:
           pot += p1.takeFromBankroll(10)
           pot += p2.takeFromBankroll(20)
       else:
           pot += p1.takeFromBankroll(20)
           pot += p2.takeFromBankroll(10)
       hand1 = deck.drawNCards(2)
       hand2 = deck.drawNCards(2)
       p1.resetLastBets()
       p2.resetLastBets()
       share = []
       minbet = 10
       callable = False
       nextUnit = self.nextUnit(p1,p2,share,hand1,hand2,deck,pot,minbet,callable,flip,round, 0)
       return(nextUnit[1], nextUnit[2])

    def playGame(self, w1, w2):
       p1 = Player.Player(2000, "p1", w1)
       p2 = Player.Player(2000, "p2", w2)
       for i in range(100):
           out = self.playHand(p1, p2, i%2==0)
           p1 = out[0]
           p2 = out[1]
           if p1.getBankroll() <= 0 or p2.getBankroll() <= 0:
               print(str(p1))
               print(str(p2))
               return
           print(str(p1) + " " + str(p2))
           print("Hand ===> " + str(i))