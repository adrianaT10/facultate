from soft_max import SoftMaxLayer
import numpy as np
from util import close_enough
from tanh import TanHLayer
from fully_connected import FcLayer
from transfer_functions import logistic, identity

def check_softmax():
    softmax = SoftMaxLayer()
    inputs = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).reshape((10, 1))

    outputs = softmax.forward(inputs)
    outputs_target = np.array([[7.80134161e-05],
                               [2.12062451e-04],
                               [5.76445508e-04],
                               [1.56694135e-03],
                               [4.25938820e-03],
                               [1.15782175e-02],
                               [3.14728583e-02],
                               [8.55520989e-02],
                               [2.32554716e-01],
                               [6.32149258e-01]])
    assert close_enough(outputs, outputs_target), "Wrong values for SoftMax forward"

    output_errors = inputs
    result = softmax.backward(inputs, output_errors)

    target_result = np.array([[-0.00065675],
                              [-0.00157318],
                              [-0.0036999],
                              [-0.00849044],
                              [-0.01882001],
                              [-0.03957987],
                              [-0.07611639],
                              [-0.12135371],
                              [-0.09731887],
                              [0.36760914]])
    assert close_enough(result, target_result), "Wrong values for SoftMax backward"

def check_tanh():
    softmax = TanHLayer()
    inputs = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).reshape((10, 1))

    outputs = softmax.forward(inputs)
    outputs_target = np.array([[0.76159416],
                               [0.96402758],
                               [0.99505475],
                               [0.9993293],
                               [0.9999092],
                               [0.99998771],
                               [0.99999834],
                               [0.99999977],
                               [0.99999997],
                               [1.]])
    assert close_enough(outputs, outputs_target), "Wrong values for Tanh forward"

    output_errors = inputs
    result = softmax.backward(inputs, output_errors)
    target_result = np.array([[4.19974342e-01],
                              [1.41301650e-01],
                              [2.95981115e-02],
                              [5.36380273e-03],
                              [9.07916155e-04],
                              [1.47459284e-04],
                              [2.32827654e-05],
                              [3.60112478e-06],
                              [5.48279254e-07],
                              [8.24461455e-08]])
    assert close_enough(result, target_result), "Wrong values for Tanh backward"

def test_linear_layer():
    l = FcLayer(4, 5, identity)
    l.weights = np.array([[0.00828426, 0.35835909, -0.26848058, 0.37474081],
                          [0.17125137, -0.10246062, 0.301141, -0.02042449],
                          [0.3111425, -0.04866925, -0.04644496, 0.05068646],
                          [-0.36114934, 0.40810522, -0.18082862, 0.01905515],
                          [0.06907316, -0.1069273, -0.35200473, -0.29067378]])
    l.biases = np.array([[-0.4146], [0.0982], [-0.3392], [0.4674], [0.0317]])

    x = np.array([[0.123], [-0.124], [0.231], [-0.400]])

    print("Testing forward computation...")
    output = l.forward(x)
    target = np.array([[-0.6699329],
                       [0.2097024],
                       [-0.32589786],
                       [0.32298011],
                       [0.0884114]])

    assert (output.shape == target.shape), "Wrong output size"
    assert close_enough(output, target), "Wrong values in layer output"
    print("Forward computation implemented ok!")

    output_err = np.array([[.001], [.001], [.99], [.001], [.001]])
    print("Testing backward computation...")
    g = l.backward(x, output_err)

    print("    i. testing gradients w.r.t. the bias terms...")
    gbias_target = np.array([[0.001],
                             [0.001],
                             [0.99],
                             [0.001],
                             [0.001]])
    assert (l.g_biases.shape == gbias_target.shape), "Wrong size"
    assert close_enough(l.g_biases, gbias_target), "Wrong values"
    print("     OK")

    print("   ii. testing gradients w.r.t. the weights...")
    gweights_target = np.array([[1.23000000e-04, -1.24000000e-04, 2.31000000e-04, -4.00000000e-04],
                                [1.23000000e-04, -1.24000000e-04, 2.31000000e-04, -4.00000000e-04],
                                [1.21770000e-01, -1.22760000e-01, 2.28690000e-01, -3.96000000e-01],
                                [1.23000000e-04, -1.24000000e-04, 2.31000000e-04, -4.00000000e-04],
                                [1.23000000e-04, -1.24000000e-04, 2.31000000e-04, -4.00000000e-04]])
    assert (l.g_weights.shape == gweights_target.shape), "Wrong size"
    assert close_enough(l.g_weights, gweights_target), "Wrong values"
    print("     OK")

    print("  iii. testing gradients w.r.t. the inputs...")
    in_target = np.array([[0.30791853],
                          [-0.04762548],
                          [-0.04648068],
                          [0.05026229]])
    assert (g.shape == in_target.shape), "Wrong size"
    assert close_enough(g, in_target), "Wrong values in input gradients"
    print("     OK")

    print("Backward computation implemented ok!")


if __name__ == "__main__":
  check_softmax()
  check_tanh()
  test_linear_layer()