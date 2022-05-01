import UnitPoker
import NeuralNetwork
import Learn
import Data

class TrainTwoNetworks(object):

    def rotateArray(self, arr):
        d = 1
        n = len(arr)
        temp = []
        i = 0
        while (i < d):
            temp.append(arr[i])
            i = i + 1
        i = 0
        while (d < n):
            arr[i] = arr[d]
            i = i + 1
            d = d + 1
        arr[:] = arr[: i] + temp
        return arr

    def train(self):
        ws = [NeuralNetwork.NeuralNetwork([],[]).randomWeights(9, 25, 6, 1), NeuralNetwork.NeuralNetwork([],[]).randomWeights(9, 25, 6, 1),NeuralNetwork.NeuralNetwork([],[]).randomWeights(9, 25, 6, 1),NeuralNetwork.NeuralNetwork([],[]).randomWeights(9, 25, 6, 1),NeuralNetwork.NeuralNetwork([],[]).randomWeights(9, 25, 6, 1),NeuralNetwork.NeuralNetwork([],[]).randomWeights(9, 25, 6, 1)]
        for i in range(100):
            open("data.txt", "w").close()
            dumbWs = ws.pop(len(ws)-1)
            ws = self.rotateArray(ws)
            ws.append(NeuralNetwork.NeuralNetwork([],[]).randomWeights(9, 25, 6, 1))
            for j in range(1, len(ws)):
                for k in range(5):
                    UnitPoker.UnitPoker().playGame(ws[0], ws[j])
            l = Learn.Learn(0.1, 10000)
            ws[0] = l.learnRecur(100000, 0.1, ws[0], Data.Data().getFileData("data.txt"))
            NeuralNetwork.NeuralNetwork(ws[0], [0]*9).networkToFile(str(i//(len(ws)-1))+"_"+str(i%(len(ws)-1)))