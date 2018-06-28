import numpy as np

from layer_interface import LayerInterface

class MaxPoolingLayer(LayerInterface):

    def __init__(self, stride):
        # Dimensions: stride
        self.stride = stride

        # indexes of max activations
        self.switches = {}

    def forward(self, inputs):
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
        (d, h, w) = inputs.shape
        errors = np.zeros((d, h, w))

        for m in range(d):
            for i in range(h / self.stride):
                for j in range(w / self.stride):
                    pos = self.switches[(m, i, j)]
                    errors[m][pos[0]][pos[1]] = output_errors[m][i][j]

        return errors

    def to_string(self):
        return "[MP (%s x %s)]" % (self.stride, self.stride)