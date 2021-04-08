import os
from json import load, dump
from neuralnetwork import NeuralNetwork
import numpy as np
from PIL import Image
<<<<<<< HEAD

def join_array(arr):
    res = []
    for i in arr:
        res.extend([int(j) for j in i])
    return np.array([res])
=======
>>>>>>> develop

NUMBER_OF_CHARS = 33
NUMBER_OF_LABELS = 2
NUMBER_OF_MARKERS = 2
TRAINING_ITERATIONS = 5000

imgs = []

def join_array(arr):
    return arr.reshape((arr.size//len(arr[0][0]), len(arr[0][0])))
def handle(path):
    classnumber = 0
    name = ''
    classnumbers = []

    img = Image.open(path)
    width = img.size[0]
    height = img.size[1]
    img = img.crop((10, 10, width-10, height-10))

    for coord in range(82, 300, 20):
        class_label = img.crop((coord, 152, coord+24, 176))
        classnumbers.append(label_sum(class_label))
    classnumber = classnumbers.index(min(classnumbers))+2
        
    '''
        label_data = is_label_on(class_label, classnum+2)
        if label_data[0]:
            classnumber_conflicts.append(label_data)
            if detected_class:
                classnumber = min(classnumber_conflicts, key=lambda x: x[1])[0]
            classnumber = classnum+2
            detected_class = True'''
        
    '''
    first_class_label = img.crop((82, 152, 106, 176))
    first_class_labelarr = np.array(first_class_label.convert('1'))
    pixels_sum_first_class_label = sum(sum(first_class_labelarr))
    imgs.append((first_class_label, pixels_sum_first_class_label))

    second_class_label = img.crop((102, 152, 126, 176))
    second_class_labelarr = np.array(second_class_label.convert('1'))
    pixels_sum_second_class_label = sum(sum(second_class_labelarr))
    imgs.append((second_class_label, pixels_sum_second_class_label))
    
    if pixels_sum_first_class_label < 525:
        classnumber = 2
    elif pixels_sum_second_class_label < 525:
        classnumber = 3'''
    assert classnumber
    return ('Иван Иванов\t'+path, classnumber, {('1', 'a'), ('2', 'b'), ('3', 'c')})

def label_sum(img):
    label_array = np.array(img.convert('1'))
    pixels_sum_label = sum(sum(label_array))
    return pixels_sum_label

def detect_blank(img):
    pass

if os.path.exists('usermode.lock'):    #checking mode for 'user' or 'develop'
    mode = 'user'
else:
    mode = 'develop'

if mode == 'user':
    char_detector = NeuralNetwork.import_from_file('char_detector.json') # loading learned nueral network
<<<<<<< HEAD
    digit_detector = NeuralNetwork.import_from_file('digit_detector.json')
    label_detector = NeuralNetwork.import_from_file('label_detector.json')
else:
    char_detector = NeuralNetwork(16*16,33)
    digit_detector = NeuralNetwork(16*16,10)
    label_detector = NeuralNetwork(16, 1)
    
    char_detector_datasets_path = input('Type path to datasets for char detector: ')
    digit_detector_datasets_path = input('Type path to datasets for digits detector: ')
    label_detector_datasets_path = input('Type path to datasets for label detector: ')
    
    if not os.path.exists(os.path.join(char_detector_datasets_path, 'set.json')):
        raise ValueError(f'Invalid dataset for char detector')
    elif not os.path.exists(os.path.join(digit_detector_datasets_path, 'set.json')):
        raise ValueError(f'Invalid dataset for digits detector')
    elif not os.path.exists(os.path.join(label_detector_datasets_path, 'set.json')):
        raise ValueError(f'Invalid dataset for label detector')
    
    digit_detector_dataset = load(open(os.path.join(digit_detector_datasets_path, 'set.json')))
    for k in digit_detector_dataset:
        img = Image.open(os.path.join(digit_detector_datasets_path, k)).convert('1')
        inputs = join_array(np.array(img))
        outputs = [np.array([[0]]) for i in range(10)]
        outputs[int(digit_detector_dataset[k])] = np.array([[1]])
        digit_detector.train(inputs, outputs, 10000)
=======
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
>>>>>>> develop
