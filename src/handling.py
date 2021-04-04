import os
from json import load, dump
from neuralnetwork import NeuralNetwork
import numpy as np
from PIL import Image

NUMBER_OF_CHARS = 33
NUMBER_OF_LABELS = 2
NUMBER_OF_MARKERS = 2
TRAINING_ITERATIONS = 5000

def join_array(arr):
    res = []
    for i in arr:
        res.extend([int(j) for j in i])
    return np.array([res])

def handle(path):
    img = Image.open(path)
    width = img.size[0]
    height = img.size[1]
    img = img.crop((10, 10, width-10, height-10))
    img2 = img.crop((82, 152, 106, 176))
    #img2.show()
    #input()
    
    return ('Иван Иванов', 7, {('1', 'a'), ('2', 'b'), ('3', 'c')})

def detect_blank(img):
    pass

if os.path.exists('usermode.lock'):    #checking mode for 'user' or 'develop'
    mode = 'user'
else:
    mode = 'develop'

if mode == 'user':
    char_detector = NeuralNetwork.import_from_file('char_detector.json') # loading learned nueral network
    #blank_markers_detector = NeuralNetwork.import_from_file('blank_markers_detector.json')
    label_detector = NeuralNetwork.import_from_file('label_detector.json')
else:
    char_detector = NeuralNetwork(16*16,NUMBER_OF_CHARS)
    label_detector = NeuralNetwork(16*16, NUMBER_OF_LABELS)
    #blank_markers_detector = NeuralNetwork(16*16, NUMBER_OF_MARKERS)
    
    char_detector_datasets_path = input('Type path to datasets for chars detector: ')
    label_detector_datasets_path = input('Type path to datasets for labels detector: ')
    #blank_markers_detector_datasets_path = input('Type path to datasets for blank markers detector: ')
    
    if not os.path.exists(os.path.join(char_detector_datasets_path, 'set.json')):           #################### CHECKING PATHS TO DATASETS ##################
        raise ValueError(f'Invalid dataset for char detector')
    #elif not os.path.exists(os.path.join(blank_markers_detector_datasets_path, 'set.json')):
        #raise ValueError(f'Invalid dataset for blank markers detector')
    elif not os.path.exists(os.path.join(label_detector_datasets_path, 'set.json')):
        raise ValueError(f'Invalid dataset for label detector')

    print('Training chars detector...')
    char_detector_dataset = load(open(os.path.join(char_detector_datasets_path, 'set.json')))
    for k in char_detector_dataset:
        print(f'Training for variant {char_detector_dataset[k]}...')
        img = Image.open(os.path.join(char_detector_datasets_path, k)).convert('1')
        img = img.resize((16, 16))
        inputs = join_array(np.array(img))
        outputs = [np.array([[0]])] * NUMBER_OF_CHARS
        outputs[int(char_detector_dataset[k])] = np.array([[1]])
        char_detector.train(inputs, outputs, TRAINING_ITERATIONS, DEBUG=True)
    
    print('Training labels detector...')
    label_detector_dataset = load(open(os.path.join(label_detector_datasets_path, 'set.json')))
    for k in label_detector_dataset:
        print(f'Training for variant {label_detector_dataset[k]}...')
        img = Image.open(os.path.join(label_detector_datasets_path, k)).convert('1')
        img = img.resize((16, 16))
        inputs = join_array(np.array(img))
        outputs = [np.array([[0]])] * NUMBER_OF_LABELS
        outputs[int(label_detector_dataset[k])] = np.array([[1]])
        label_detector.train(inputs, outputs, TRAINING_ITERATIONS, DEBUG=True)

    '''
    print('Training blank_markers detector...')
    blank_markers_detector_dataset = load(open(os.path.join(blank_markers_detector_datasets_path, 'set.json')))
    for k in blank_markers_detector_dataset:
        print(f'Training for variant {blank_markers_detector_dataset[k]}...')
        img = Image.open(os.path.join(blank_markers_detector_datasets_path, k)).convert('1')
        img = img.resize((16, 16))
        inputs = join_array(np.array(img))
        outputs = [np.array([[0]])] * NUMBER_OF_MARKERS
        outputs[int(blank_markers_detector_dataset[k])] = np.array([[1]])
        blank_markers_detector.train(inputs, outputs, TRAINING_ITERATIONS, DEBUG=True)'''

    char_detector.export_to_file('char_detector.json')  # saving learned nueral network
    label_detector.export_to_file('label_detector.json')
    #blank_markers_detector.export_to_file('blank_markers_detector.json')
    print('Networks trained!')
