import os
from neuralnetwork import NeuralNetwork

def handle(path):
    print(path)
    for i in range(1000000):pass
    return ('Иван Иванов', {('a', '1'), ('b', '2'), ('c', '3')})

if os.path.exists('usermode.lock'):    #checking mode for 'user' or 'develop'
    mode = 'user'
else:
    mode = 'develop'

n = NeuralNetwork.import_from_file('neuralnetwork.json')
