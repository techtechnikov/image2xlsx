import numpy as np
from json import load, dump

class Neuron():
    def __init__(self, number_of_synaps=10):
        self.weights = 2 * np.random.random((number_of_synaps, 1)) - 1

        self.sigmoid = lambda x: 1 / (1 + np.exp(-x))
        self.sigmoid_deriv = lambda x: x * (1 - x)

    def train(self, inputs, outputs, number_of_training_iterations):
        progress = 0
        for i in range(number_of_training_iterations):
            output = self.think(inputs)
            error = outputs - output
            adj = np.dot(inputs.T, error * self.sigmoid_deriv(output))
            self.weights += adj
            progress += 1

    def think(self, inputs):
        return self.sigmoid(np.dot(inputs, self.weights))

    def __str__(self):
        return f'Neuron({len(self.weights)})'

    def __repr__(self):
        return self.__str__()

class NeuralNetwork:
    def __init__(self, number_of_synaps=10, number_of_neurons_in_layer=10, number_of_layers=1):
        self.layer = [Neuron(number_of_synaps)  for i in range(number_of_neurons_in_layer)]
        self.number_of_synaps = number_of_synaps

    def train(self, inputs, outputs, number_of_training_iterations, DEBUG=False):
        for i, n in enumerate(self.layer):
            if DEBUG: print(f'Training neuron {i}...', end='\n'+('- '*40)+'\n')
            n.train(inputs, outputs[i], number_of_training_iterations)


    def think(self, inputs):
        return [n.think(inputs) for n in self.layer]

    def export_to_file(self, path):
        file = open(path, 'w')
        data = {}
        data['number_of_synaps'] = self.number_of_synaps
        data['layer'] = {}
        for i, n in enumerate(self.layer):
            data['layer'][str(i)] = {'weights':repr(n.weights)}
        dump(data, file)
        file.close()

    @staticmethod
    def import_from_file(path):
        file = open(path)
        data = load(file)
        network = NeuralNetwork()
        network.layer = []
        number_of_synaps = data['number_of_synaps']
        network.number_of_synaps = number_of_synaps
        for k in data['layer']:
            n = Neuron(number_of_synaps)
            n.weights = eval('np.'+data['layer'][k]['weights'])
            network.layer.append(n)
        file.close()
        return network
