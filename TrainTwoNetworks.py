import UnitPoker
import NeuralNetwork
import LogisticRegression
import SVM
import Learn
import Data
import json

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
        data = self.getDataFromFile()
        ws = [data, data, data, data, data]
        for i in range(100):
            dumbWs = ws.pop(len(ws)-1)
            ws = self.rotateArray(ws)
            ws.append(data)
            open("data.txt", "w").close()
            for j in range(1, len(ws)):
                print(j)
                UnitPoker.UnitPoker().playGame(ws[0], ws[j])
            data = self.getDataFromFile()
            ws[0] = data
            SVM.SVM(data).networkToFile(str(i//(len(ws)-1))+"_"+str(i%(len(ws)-1)))
            
    def getDataFromFile(self):
        file = open("data.txt", "r")
        lines = file.readlines()
        data = []
        for i in range(0, min(len(lines), 100000000000000000000), 2):
            data.append([json.loads(lines[i]), json.loads(lines[i+1])])
        return data