
import sys
import csv

import math
import operator
import itertools

from sys import argv



def get_distance(point_1, point_2):
    distance = 0
    for key in point_1:
        if key == 'Class':
            continue
        distance += abs(point_1[key] - point_2[key])
    return distance


training_data = sys.argv[1]
testing_data = sys.argv[2]
k = int(sys.argv[3])

is_first_line = True
features = []
number_of_features = 0
training_dataset = []

# Load training dataset to memory.
with open(training_data) as training_data_handler:
    for line in training_data_handler:
        if is_first_line:  # Only enter for the first line which contains the name of the features
            clean_line = ''
            for char in line:
                if char not in '"':
                    clean_line += char
            features = clean_line.split()
            is_first_line = False
            number_of_features = len(features)
            continue
        words = line.split()
        values = []
        for word in words:
            values.append(float(word))
        if len(values) != number_of_features:
            raise ValueError('Number of values do not match number of features. Error in line: ', line)
        else:  # Enter if line contains data
            row = {}
            for i in range(number_of_features):
                row[features[i]] = values[i]
            training_dataset.append(row)

# Load testing dataset to memory.
testing_dataset = []
is_first_line = True
with open(testing_data) as testing_data_handler:
    for line in testing_data_handler:
        if is_first_line:
            is_first_line = False
            continue
        words = line.split()
        values = []
        for word in words:
            values.append(float(word))
        if len(values) != number_of_features - 1:
            raise ValueError('Number of values do not match number of features. Error in line: ', line)
        else:  # Enter if line contains data
            row = {}
            for i in range(number_of_features - 1):
                row[features[i]] = values[i]
            row['Class'] = None
            testing_dataset.append(row)

for row in testing_dataset:
    distances = {}
    for data_point in training_dataset:
        distances[get_distance(row, data_point)] = int(data_point['Class'])
    neighbourhood_classes = []
    for key, value in dict(sorted(distances.items())).items():
        neighbourhood_classes.append(value)

    class_frequency = {}
    for neighbour_class in neighbourhood_classes[:k]:
        class_frequency[neighbour_class] = class_frequency.get(neighbour_class, 0) + 1
    print(dict(sorted(class_frequency.items())))
    # print(sorted(class_frequency.items())[0])