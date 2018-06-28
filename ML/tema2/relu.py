import numpy as np
from transfer_functions import relu

from layer_interface import LayerInterface

class ReluLayer(LayerInterface):

    def __init__(self):
        pass

    def forward(self, inputs):
        self.outputs = relu(inputs)
        return self.outputs


    def backward(self, inputs, output_errors):
        return output_errors * relu(self.outputs, True)


    def to_string(self):
        return "[Relu]"
