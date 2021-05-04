import numpy as np
import math


class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.alpha = alpha
        self.labels = []
        self.table = []
        self.p_labels = []

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        self.labels = [label for label in set(y)]
        classes = len(self.labels)
        c_labels = [0] * classes
        for i in range(len(y)):
            y[i] = self.labels.index(y[i]) + 1
            c_labels[y[i] - 1] += 1
        self.table = [[] for _ in range(classes * 2 + 1)]
        self.p_labels = [math.log(count / sum(c_labels)) for count in c_labels]
        for i in range(len(X)):
            words = X[i].split()
            for word in words:
                if word in self.table[0]:
                    self.table[y[i]][self.table[0].index(word)] += 1
                else:
                    self.table[0].append(word)
                    self.table[y[i]].append(1)
                    index = y[i]
                    for j in range(classes - 1):
                        index = (index % classes) + 1
                        self.table[index].append(0)
                    for column in range(classes + 1, classes * 2 + 1):
                        self.table[column].append(0)
        s_table = [sum(self.table[i + 1]) for i in range(classes)]
        for line in range(len(self.table[0])):
            for column in range(classes + 1, classes * 2 + 1):
                self.table[column][line] = (self.table[column -
                    classes][line] + self.alpha) / (s_table[column
                    - classes - 1] + self.alpha * len(self.table[0]))

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        labels = []
        classes = len(self.labels)
        for string in X:
            string_labels = [p_label for p_label in self.p_labels]
            words = string.split()
            for word in words:
                if word in self.table[0]:
                    for i in range(classes):
                        string_labels[i] += math.log(self.table[i + classes + 1]
                        [self.table[0].index(word)])
            for i in range(classes):
                if string_labels[i] == max(string_labels):
                    labels.append(self.labels[i])
                    break
        return labels

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        prediction = self.predict(X_test)
        count = 0
        for i in range(len(prediction)):
            if prediction[i] == y_test[i]:
                count += 1
        score = count / len(y_test)
        return score
