import matplotlib.pyplot as plt
import pickle
import os

class Plot():

    def __init__(self):
        self.line_types = ["-r","-g","-b","-y"]
    
    def plot(self):
        infos = []
        i=0
        for x in os.listdir("info/"):
            f = open("info/"+x,'rb')
            inf = pickle.load(f)
            plt.plot(inf[0],inf[2],self.line_types[i], label=x.split('.')[0])
            i+=1
        plt.legend()
        plt.ylabel("Waiting Time (ms)")
        plt.xlabel("Step")
        plt.suptitle('100 Vehicles', fontsize=12)
        plt.show()