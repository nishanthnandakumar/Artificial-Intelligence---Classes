#! /usr/bin/env python
import numpy as np

def perceptronlearning(pos_class,neg_class):
    w = [1,1]
    class_pos = []
    class_neg = []

    while True:

        for i in range(len(pos_class)):
            class_pos = class_pos + np.dot(w , pos_class[i])
            if  np.dot(w , pos_class[i]) <= 0:
                w = np.add(w , pos_class[i])

        for i in range(len(neg_class)):
            class_neg = class_neg + np.dot(w , neg_class[i])
            if np.dot(w , neg_class[i]) >= 0:
                w = np.subtract(w,neg_class[i])

        if all(i > 0 for i in class_pos) and all(i < 0 for i in class_neg):
            return w

# [[6,1],[7,3],[8,2],[9,0]]
#[[8,4],[8,6],[9,2],[9,5]]

M_pos = [[0,1.8],[2,0.6]]

M_neg = [[-1.2,1.4],[0.4,-1]]

weights = perceptronlearning(M_pos, M_neg)
print(weights)
