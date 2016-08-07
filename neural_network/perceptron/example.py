# -*- coding: utf-8 -*-

import numpy as np

from perceptron import Perceptron

in_data = np.array([[1, 0, 0, -1],
                    [1, 0, 1, 1],
                    [1, 1, 0, 1],
                    [1, 1, 1, 1],
                    [0, 0, 1, -1],
                    [0, 1, 0, -1],
                    [0, 1, 1, 1],
                    [0, 0, 0, -1]])

perc = Perceptron()
perc.training_alg(in_data[:, :3], in_data[:, -1])

print perc.inference(in_data[:, :3])
