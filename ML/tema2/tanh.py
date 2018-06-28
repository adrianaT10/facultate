from layer_interface import LayerInterface
from transfer_functions import hyperbolic_tangent

class TanHLayer(LayerInterface):
    def __init__(self):
        pass

    def forward(self, inputs):
        self.outputs = hyperbolic_tangent(inputs)
        return self.outputs


    def backward(self, inputs, output_errors):
        delta = output_errors * hyperbolic_tangent(self.outputs, True)
        return delta


    def to_string(self):
        return "[TanH]"