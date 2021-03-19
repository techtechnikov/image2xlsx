import os
from neuralnetwork import NeuralNetwork

def handle(path):
    print(path)
    for i in range(1000000):pass
    return ('Иван Иванов', 7, {('1', 'a'), ('2', 'b'), ('3', 'c')})

if os.path.exists('usermode.lock'):    #checking mode for 'user' or 'develop'
    mode = 'user'
else:
    mode = 'develop'

if mode == 'user1':
    n = NeuralNetwork.import_from_file('neuralnetwork.json') # loading learned nueral network
else:
    n = NeuralNetwork(43)
