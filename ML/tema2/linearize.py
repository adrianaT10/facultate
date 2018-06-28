import numpy as np

from layer_interface import LayerInterface

class LinearizeLayer(LayerInterface):

    def __init__(self, depth, height, width):
        # Dimensions: depth, height, width
        self.depth = depth
        self.height = height
        self.width = width


    def forward(self, inputs):
        assert(inputs.shape == (self.depth, self.height, self.width))

        # Reshape inputs- transform volume to column
        self.outputs = inputs.reshape(self.depth * self.height * self.width, 1)
        return self.outputs

    def backward(self, inputs, output_errors):
        # unused argument - inputs
        assert(output_errors.shape == (self.depth * self.height * self.width, 1))

        # Reshape gradients - transform column to volume
        return output_errors.reshape((self.depth, self.height, self.width))

    def to_string(self):
        return "[Lin ((%s, %s, %s) -> %s)]" % (self.depth, self.height, self.width, self.depth * self.height * self.width)


class LinearizeLayerReverse(LayerInterface):

    def __init__(self, depth, height, width):
        # Dimensions: depth, height, width
        self.depth = depth
        self.height = height
        self.width = width


    def forward(self, inputs):
        assert(inputs.shape == (self.depth * self.height * self.width, 1))

        # Reshape inputs - transform column to volume
        self.outputs = inputs.reshape((self.depth, self.height, self.width))
        return self.outputs

    def backward(self, inputs, output_errors):
        # unused argument - inputs
        assert(output_errors.shape == (self.depth, self.height, self.width))

        # Reshape gradients - transform volume to column
        return output_errors.reshape(self.depth * self.height * self.width, 1)

    def to_string(self):
        return "[Lin (%s -> (%s, %s, %s))]" % (self.depth * self.height * self.width, self.depth, self.height, self.width)
