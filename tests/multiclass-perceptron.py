import unittest
from itertools import izip
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets

from layers import LinearLayer, SigmoidLayer
from loss import SquaredLoss, SoftmaxNLL
from optim import RMSProp, AdaGrad, MomentumSGD, SGD
from sequential import SequentialModel


def gen_data():
    n = 100

    # N clusters:
    data, targets = datasets.make_classification(
        n_samples=n, n_features=2, n_informative=2, n_redundant=0, n_classes=3, class_sep=3.0, n_clusters_per_class=1)

    # Circles:
    # data, targets = datasets.make_circles(
    #     n_samples=n, shuffle=True, noise=0.05, random_state=None, factor=0.1)

    # Moons:
    # data, targets = datasets.make_moons(n_samples=n, shuffle=True, noise=0.05)

    train_data, test_data = data[:n / 2], data[n / 2:]
    train_targets, test_targets = targets[:n / 2], targets[n / 2:]

    # Scatter train_data
    x0 = [point[0] for i, point in enumerate(train_data) if train_targets[i] == 0]
    y0 = [point[1] for i, point in enumerate(train_data) if train_targets[i] == 0]
    x1 = [point[0] for i, point in enumerate(train_data) if train_targets[i] == 1]
    y1 = [point[1] for i, point in enumerate(train_data) if train_targets[i] == 1]
    x2 = [point[0] for i, point in enumerate(train_data) if train_targets[i] == 2]
    y2 = [point[1] for i, point in enumerate(train_data) if train_targets[i] == 2]

    plt.figure(1)
    plt.scatter(x0, y0, color='gray', marker="o", s=100)
    plt.scatter(x1, y1, color='gray', marker="x", s=100)
    plt.scatter(x2, y2, color='gray', marker="v", s=100)

    return train_data, train_targets, test_data, test_targets


def scatter_test_data(data, target, model):
    plt.figure(1)
    colors = ['r', 'g', 'b', 'y', 'o']
    color = lambda t: colors[t]

    for x, target in izip(data, target):
        y = model.forward(x)
        target_class = np.argmax(y)
        plt.scatter(x[0], x[1], s=40, c=color(target_class))


class Perceptron(unittest.TestCase):
    def test_Perceptron(self):
        train_data, train_targets, test_data, test_targets = gen_data()

        model = SequentialModel([
            LinearLayer(2, 3, initialize='random'),
        ])

        model.learn_minibatch(input_data=train_data,
                    target_data=train_targets,
                    loss=SoftmaxNLL(),
                    batch_size=5,

                    optimizer=SGD(learning_rate=0.1),
                    # optimizer=MomentumSGD(learning_rate=0.1, momentum=0.9),
                    # optimizer=AdaGrad(learning_rate=0.9),
                    # optimizer=RMSProp(learning_rate=0.1, decay_rate=0.9),

                    epochs=200,
                    save_progress=True)

        scatter_test_data(test_data, test_targets, model)

        model.plot_errors_history()
        model.plot_loss_gradient_history()
        plt.show()
