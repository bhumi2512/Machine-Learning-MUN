import csv
import math
import operator
import itertools
import sys
from sys import argv
from collections import Counter


# function to load training and test data

def loadDataSet(trainingFileName, testFileName, trainingDataSet=[], testDataSet=[]):
    tempTrainingDataSet = []
    tempTestDataSet = []
    num_cols = 0

    try:
        with open(trainingFileName, 'r') as trainingfile:
            fileLines = trainingfile.readline()
            lines = csv.reader(trainingfile, delimiter='\t')

            num_cols = len(fileLines.split())

            for row in itertools.islice(lines, 0, None):
                tempTrainingDataSet.append(row)

            trainingDataset = list(tempTrainingDataSet)

            for x in range(len(trainingDataset)):
                for y in range(num_cols - 1):
                    trainingDataset[x][y] = float(trainingDataset[x][y])

                trainingDataSet.append(trainingDataset[x])

        with open(testFileName, 'r') as testfile:
            fileLines = testfile.readline()
            lines = csv.reader(testfile, delimiter='\t')

            num_cols = len(fileLines.split())

            for row in itertools.islice(lines, 0, None):
                tempTestDataSet.append(row)

            testDataset = list(tempTestDataSet)

            for x in range(len(testDataset)):
                for y in range(num_cols):
                    testDataset[x][y] = float(testDataset[x][y])

                testDataSet.append(testDataset[x])
    except FileNotFoundError as e:
        print("An Exception Occured : {}".format(e))
    except:
        print("An Exception Occured")

    # Method to calculate eculidean distance


def eculideanDistance(datapoint1, datapoint2, length):
    pointDistance = 0
    for x in range(length):
        pointDistance += pow((datapoint1[x] - datapoint2[x]), 2)
    return math.sqrt(pointDistance)


# Method to get neighbors

def filterNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance) - 1

    for x in range(len(trainingSet)):
        dist = eculideanDistance(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x], dist))

    distances.sort(key=operator.itemgetter(1))
    neighbors = []

    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors


def getResponse(neighbors):
    try:
        classVotes = {}
        for x in range(len(neighbors)):
            response = neighbors[x][-1]
            if response in classVotes:
                classVotes[response] += 1
            else:
                classVotes[response] = 1

        sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)

    except NameError as e:
        print("An Exception Occured : {}".format(e))
    except:
        print("An Exception Occured")

    return sortedVotes[0][0]


# get calculate class probability

def getProbability(neighbors, classElement):
    try:
        class_counter = Counter()
        for neighbor in neighbors:
            class_counter[neighbor[9]] += 1

        labels, votes = zip(*class_counter.most_common())
        commonClass = class_counter.most_common(1)[0][0]
        votesClass = class_counter.most_common(1)[0][1]
        # return commonClass, votesClass/sum(votes)
        eProbability = votesClass / sum(votes)
        print(classElement + '\t' + '{0:.2f}'.format(eProbability))

    except:
        print("An Exception Occured")


def main():
    # read shell argument
    trainingDataSet = []
    testDataSet = []
    kNearest = ''

    try:
        if len(argv) >= 3:
            trainingFileName = argv[1]
            testFileName = argv[2]

        if len(argv) == 4:
            kNearest = argv[3]

    except IndexError:
        print("Excepted training and test file name as an argument.")
    except ValueError as e:
        print("An Exception Occured : {}".format(e))
    except:
        print("An Exception Occured")
    else:
        try:
            # prepare data
            loadDataSet(trainingFileName, testFileName, trainingDataSet, testDataSet)

            # generate predictions
            if len(kNearest) <= 0:
                k = 3
            else:
                k = int(kNearest)

            predictedClass = []

            for x in range(len(testDataSet)):
                neighbors = filterNeighbors(trainingDataSet, testDataSet[x], k)
                result = getResponse(neighbors)
                predictedClass.append(int(result))

                # call conditional probability
                getProbability(neighbors, result)

        except ValueError as e:
            print("An Exception Occured : {}".format(e))


if __name__ == "__main__":
    main()