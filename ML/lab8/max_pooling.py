import numpy as np

from layer_interface import LayerInterface

class MaxPoolingLayer(LayerInterface):

    def __init__(self, stride):
        # Dimensions: stride
        self.stride = stride

        # indexes of max activations
        self.switches = {}

    def forward(self, inputs):

        # TODO 3
        (d, h, v) = inputs.shape
        self.outputs = np.zeros((d, h / self.stride, v / self.stride))
        for m in range(d):
            for i in range(h / self.stride):
                for j in range(v / self.stride):
                    aux = np.array(inputs[m, i*self.stride:(i+1)*self.stride, j*self.stride:(j+1)*self.stride])
                    self.outputs[m][i][j] = np.amax(aux)
                    n = np.argmax(aux)
                    self.switches[(m, i, j)] = (i*self.stride + n/self.stride, j*self.stride + n - n/self.stride - 1)
        return self.outputs

    def backward(self, inputs, output_errors):

        # TODO 3
        (d, h, w) = inputs.shape
        errors = np.zeros((d, h, w))

        for m in range(d):
            for i in range(h / self.stride):
                for j in range(w / self.stride):
                    pos = self.switches[(m, i, j)]
                    errors[m][pos[0]][pos[1]] = output_errors[m][i][j]

        print errors
        return errors

    def to_string(self):
        return "[MP (%s x %s)]" % (self.stride, self.stride)

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

from util import close_enough

def test_max_pooling_layer():

    l = MaxPoolingLayer(2)

    x = np.array([[[1, 2, 3, 4], [5, 6, 7, 8]],
                  [[9, 10, 11, 12], [13, 14, 15, 16]],
                  [[17, 18, 19, 20], [21, 22, 23, 24]]])

    print("Testing forward computation...")
    output = l.forward(x)
    target = np.array([[[6, 8]],
                       [[14, 16]],
                       [[22, 24]]])
    assert (output.shape == target.shape), "Wrong output size"
    assert close_enough(output, target), "Wrong values in layer ouput"
    print("Forward computation implemented ok!")


    output_err = output

    print("Testing backward computation...")

    g = l.backward(x, output_err)
    print(g)


    print("Testing gradients")
    in_target = np.array([[[0, 0, 0, 0], [0, 6, 0, 8]],
                          [[0, 0, 0, 0], [0, 14, 0, 16]],
                          [[0, 0, 0, 0], [0, 22, 0, 24]]])

    assert (g.shape == in_target.shape), "Wrong size"
    assert close_enough(g, in_target), "Wrong values in gradients"
    print("     OK")

    print("Backward computation implemented ok!")


if __name__ == "__main__":
    test_max_pooling_layer()
