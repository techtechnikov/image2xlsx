import os
from json import load, dump
from neuralnetwork import NeuralNetwork
import numpy as np
from PIL import Image

NUMBER_OF_CHARS = 33
NUMBER_OF_LABELS = 2
NUMBER_OF_MARKERS = 2
TRAINING_ITERATIONS = 5000
ABC = 'абвгд'

imgs = []

def join_array(arr):
    return arr.reshape((arr.size//arr[0][0].size, arr[0][0].size))
def handle(path):
    global imgs
    classnumber = 0
    name = ''
    classnumbers = []

    img = Image.open(path)
    width = img.size[0]
    height = img.size[1]
    img = img.crop((10, 10, width-10, height-10))

    pixel = 0
    for i in join_array(np.array(img.convert('L'))):
        pixel += i[0]
    pixel = pixel//np.array(img.convert('L')).size

    for coord in range(82, 300, 23):
        class_label = img.crop((coord, 152, coord+24, 176))
        classnumbers.append(label_sum(class_label))
    classnumber = classnumbers.index(min(classnumbers))+2

    answers = []
    for n1, coord_ans in enumerate(range(47, 350, 152)):
        for n, coord_checkbox_vert in enumerate(range(0, 78, 17)):
            answers_labs = []
            for coord_checkbox in range(0, 78, 17):            
                ans_label = img.crop((coord_ans+coord_checkbox_vert-10, coord_checkbox+240-10, coord_ans+coord_checkbox_vert+18-10, coord_checkbox+240+18-10))
                answers_labs.append(label_sum(ans_label))
                imgs.append(ans_label)
            answers.append((n+(n1*5)+1, ABC[answers_labs.index(min(answers_labs))]))
            
    for n1, coord_ans in enumerate(range(47, 350, 152)):
        for n, coord_checkbox_vert in enumerate(range(0, 78, 17)):
            answers_labs = []
            for coord_checkbox in range(0, 78, 17):            
                ans_label = img.crop((coord_ans+coord_checkbox_vert-10, coord_checkbox+343-10, coord_ans+coord_checkbox_vert+18-10, coord_checkbox+343+18-10))
                answers_labs.append(label_sum(ans_label))
                imgs.append(ans_label)
            answers.append((n+15+1+(n1*5), ABC[answers_labs.index(min(answers_labs))]))
    assert classnumber
    return ('Иван Иванов\t'+path, classnumber, set([tuple(ans) for ans in answers]))

def label_sum(img):
    label_array = np.array(img.convert('1'))
    pixels_sum_label = sum(sum(label_array))
    return pixels_sum_label

if os.path.exists('usermode.lock'):    #checking mode for 'user' or 'develop'
    mode = 'user'
else:
    mode = 'develop'

if mode == 'user':
    char_detector = NeuralNetwork.import_from_file('char_detector.json') # loading learned nueral network
    label_detector = NeuralNetwork.import_from_file('label_detector.json')
else:
    char_detector = NeuralNetwork(16*16,NUMBER_OF_CHARS)
    label_detector = NeuralNetwork(16*16, NUMBER_OF_LABELS)
    
    char_detector_datasets_path = input('Type path to datasets for chars detector: ')
    label_detector_datasets_path = input('Type path to datasets for labels detector: ')
    
    if not os.path.exists(os.path.join(char_detector_datasets_path, 'set.json')):           #################### CHECKING PATHS TO DATASETS ##################
        raise ValueError(f'Invalid dataset for char detector')
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


    char_detector.export_to_file('char_detector.json')  # saving learned nueral network
    label_detector.export_to_file('label_detector.json')
    print('Networks trained!')
