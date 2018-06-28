from layer_interface import LayerInterface
import numpy as np

class SoftMaxLayer(LayerInterface):
	def __init__(self):
		pass

	def forward(self, inputs):
		self.outputs = np.zeros(len(inputs))

		aux_sum = np.sum(np.e ** inputs)

		self.outputs = (np.e ** inputs) / aux_sum
		return self.outputs

	def backward(self, inputs, output_errors):
		z = np.sum(self.outputs * output_errors)
		delta = self.outputs * (output_errors - z)

		return delta