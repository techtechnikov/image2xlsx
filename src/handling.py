import os
from json import load, dump
from neuralnetwork import NeuralNetwork
import numpy as np
from PIL import Image

NUMBER_OF_DIGITS = 10
NUMBER_OF_CHARS = 33
TRAINING_ITERATIONS = 5000

def join_array(arr):
    res = []
    for i in arr:
        res.extend([int(j) for j in i])
    return np.array([res])

def handle(path):
    print(path)
    for i in range(1000000):pass
    return ('Иван Иванов', 7, {('1', 'a'), ('2', 'b'), ('3', 'c')})

def detect_blank(img):
    pass

if os.path.exists('usermode.lock'):    #checking mode for 'user' or 'develop'
    mode = 'user'
else:
    mode = 'develop'

if mode == 'user':
    char_detector = NeuralNetwork.import_from_file('char_detector.json') # loading learned nueral network
    digit_detector = NeuralNetwork.import_from_file('digit_detector.json')
    label_detector = NeuralNetwork.import_from_file('label_detector.json')
else:
    char_detector = NeuralNetwork(16*16,NUMBER_OF_CHARS)
    digit_detector = NeuralNetwork(16*16,NUMBER_OF_DIGITS)
    label_detector = NeuralNetwork(16, 1)
    '''
    char_detector_datasets_path = input('Type path to datasets for char detector: ')
    digit_detector_datasets_path = input('Type path to datasets for digits detector: ')
    label_detector_datasets_path = input('Type path to datasets for label detector: ')
    
    if not os.path.exists(os.path.join(char_detector_datasets_path, 'set.json')):           #################### CHECKING PATHS TO DATASETS ##################
        raise ValueError(f'Invalid dataset for char detector')
    elif not os.path.exists(os.path.join(digit_detector_datasets_path, 'set.json')):
        raise ValueError(f'Invalid dataset for digits detector')
    elif not os.path.exists(os.path.join(label_detector_datasets_path, 'set.json')):
        raise ValueError(f'Invalid dataset for label detector')

    print('Training digits detector...')
    digit_detector_dataset = load(open(os.path.join(digit_detector_datasets_path, 'set.json')))
    for k in digit_detector_dataset:
        img = Image.open(os.path.join(digit_detector_datasets_path, k)).convert('1')
        inputs = join_array(np.array(img))
        outputs = [np.array([[0]]) for i in range(NUMBER_OF_DIGITS)]
        outputs[int(digit_detector_dataset[k])] = np.array([[1]])
        digit_detector.train(inputs, outputs, TRAINING_ITERATIONS)

    print('Training chars detector...')
    char_detector_dataset = load(open(os.path.join(char_detector_datasets_path, 'set.json')))
    for k in char_detector_dataset:
        img = Image.open(os.path.join(char_detector_datasets_path, k)).convert('1')
        inputs = join_array(np.array(img))
        outputs = [np.array([[0]]) for i in range(NUMBER_OF_CHARS)]
        outputs[int(char_detector_dataset[k])] = np.array([[1]])
        char_detector.train(inputs, outputs, TRAINING_ITERATIONS)
    
    print('Training labels detector...')
    label_detector_dataset = load(open(os.path.join(label_detector_datasets_path, 'set.json')))
    for k in label_detector_dataset:
        img = Image.open(os.path.join(label_detector_datasets_path, k)).convert('1')
        inputs = join_array(np.array(img))
        outputs = [np.array([[0]])]
        outputs[int(label_detector_dataset[k])] = np.array([[1]])
        label_detector.train(inputs, outputs, TRAINING_ITERATIONS)

    char_detector.export_to_file('char_detector.json')  # saving learned nueral network
    digit_detector.export_to_file('digit_detector.json')
    label_detector.export_to_file('label_detector.json')'''
