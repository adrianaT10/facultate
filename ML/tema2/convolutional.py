import numpy as np

from layer_interface import LayerInterface

class ConvolutionalLayer(LayerInterface):

    def __init__(self, inputs_depth, inputs_height, inputs_width, outputs_depth, k, stride):
        # Number of inputs, number of outputs, filter size, stride

        self.inputs_depth = inputs_depth
        self.inputs_height = inputs_height
        self.inputs_width = inputs_width

        self.k = k
        self.stride = stride

        self.outputs_depth = outputs_depth
        self.outputs_height = int((self.inputs_height - self.k) / self.stride + 1)
        self.outputs_width = int((self.inputs_width - self.k) / self.stride + 1)


        # Layer's parameters
        self.weights = np.random.normal(
            0,
            np.sqrt(2.0 / float(self.outputs_depth + self.inputs_depth + self.k + self.k)),
            (self.outputs_depth, self.inputs_depth, self.k, self.k)
        )
        self.biases = np.random.normal(
            0,
            np.sqrt(2.0 / float(self.outputs_depth + 1)),
            (self.outputs_depth, 1)
        )

        # Computed values
        self.outputs = np.zeros((self.outputs_depth, self.outputs_height, self.outputs_width))

        # Gradients
        self.g_weights = np.zeros(self.weights.shape)
        self.g_biases = np.zeros(self.biases.shape)

        # Delta for momentum
        self.delta_weights = np.zeros(self.weights.shape)
        self.delta_biases = np.zeros(self.biases.shape)


    def im2col(self, im):
        X = []
        for i in range(self.outputs_height):
            for j in range(self.outputs_width):
                X.append(im[:, i * self.stride : i * self.stride + self.k, j*self.stride : j*self.stride + self.k].reshape(self.inputs_depth * self.k * self.k))

        X = np.array(X).T
        return X

    def col2im(self, m):
        X = np.zeros((self.inputs_depth, self.inputs_height, self.inputs_width))

        for i in range(0, self.outputs_height):
            for j in range(0, self.outputs_width):
                X[:, i * self.stride : i*self.stride + self.k, j*self.stride : j * self.stride + self.k] += \
                    m[i*self.outputs_width + j].reshape(self.inputs_depth, self.k, self.k)
        return X



    def forward(self, inputs):
        assert(inputs.shape == (self.inputs_depth, self.inputs_height, self.inputs_width))

        # -> compute self.a and self.outputs
        W = self.weights.reshape(self.outputs_depth, -1)
        X = self.im2col(inputs)

        self.outputs = np.dot(W, X) + self.biases
        self.outputs = self.outputs.reshape(self.outputs_depth, self.outputs_height, self.outputs_width)

        return self.outputs

    def backward(self, inputs, output_errors):
        assert(output_errors.shape == (self.outputs_depth, self.outputs_height, self.outputs_width))

        # Compute the gradients w.r.t. the bias terms (self.g_biases)
        self.g_biases = np.sum(output_errors, axis=(1, 2))
        self.g_biases = self.g_biases.reshape(self.outputs_depth, -1)

        # Compute the gradients w.r.t. the weights (self.g_weights)
        D = output_errors.reshape(self.outputs_depth, -1)
        X = self.im2col(inputs)

        self.g_weights = np.dot(D, X.T).reshape(self.outputs_depth, self.inputs_depth, self.k, self.k)

        # Compute and return the gradients w.r.t the inputs of this layer
        delta = np.zeros((self.inputs_depth, self.inputs_height, self.inputs_width))

        W = self.weights.reshape(self.outputs_depth, -1)
        delta = np.dot(D.T, W)
        delta = self.col2im(delta)

        return delta


    def update_parameters(self, learning_rate, momentum):
        self.delta_biases = -learning_rate * self.g_biases + momentum * self.delta_biases
        self.biases += self.delta_biases

        self.delta_weights = -learning_rate * self.g_weights + momentum * self.delta_weights
        self.weights += self.delta_weights

    def to_string(self):
        return "[C ((%s, %s, %s) -> (%s, %s ) -> (%s, %s, %s)]" % (self.inputs_depth, self.inputs_height, self.inputs_width, self.k, self.stride, self.outputs_depth, self.outputs_height, self.outputs_width)

from util import close_enough

def test_convolutional_layer():

    np.random.seed(0)

    l = ConvolutionalLayer(2, 3, 4, 3, 2, 1)


    l.weights = np.random.rand(3, 2, 2, 2)

    l.biases = np.random.rand(3, 1)

    x = np.array([[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
                  [[13, 14, 15, 16], [17, 18, 19, 20], [21, 22, 23, 24]]])

    print("Testing forward computation...")
    output = l.forward(x)
    target = np.array([[[ 34.55043437, 38.95942899, 43.36842361],
                        [ 52.18641284, 56.59540746, 61.00440208]],
    [[ 30.72457988, 34.08923073, 37.45388158],
     [ 44.18318328, 47.54783413, 50.91248498]],
     [[ 28.2244684, 31.30220961, 34.37995083],
      [ 40.53543326, 43.61317448, 46.69091569]]])
    assert (output.shape == target.shape), "Wrong output size"
    assert close_enough(output, target), "Wrong values in layer ouput"
    print("Forward computation implemented ok!")

    output_err = np.random.rand(3, 2, 3)

    print("Testing backward computation...")

    g = l.backward(x, output_err)
#    print(l.g_biases)
#    print(l.g_weights)
#    print(g)

    print("    i. testing gradients w.r.t. the bias terms...")
    gbias_target =  np.array([[ 2.4595299 ],
                              [ 3.86207926],
                              [ 1.17504241]])

    assert (l.g_biases.shape == gbias_target.shape), "Wrong size"
    assert close_enough(l.g_biases, gbias_target), "Wrong values"
    print("     OK")

    print("   ii. testing gradients w.r.t. the weights...")
    gweights_target = np.array(
            [[[[ 12.19071134, 14.65024124],
               [ 22.02883093, 24.48836083]],
    [[ 41.70507011, 44.1646    ],
     [ 51.54318969, 54.00271959]]],

    [[[ 17.14269456, 21.00477382],
      [ 32.59101161, 36.45309087]],

  [[ 63.4876457 , 67.34972496],
   [ 78.93596275, 82.79804201]]],

 [[[  5.38434096,  6.55938337],
   [ 10.08451061, 11.25955302]],

  [[ 19.4848499 , 20.65989231],
   [ 24.18501955, 25.36006196]]]]
    )

    assert (l.g_weights.shape == gweights_target.shape), "Wrong size"
    assert close_enough(l.g_weights, gweights_target), "Wrong values"
    print("     OK")


    print("  iii. testing gradients w.r.t. the inputs...")
    in_target = np.array(
[[[ 0.1873886 , 1.2046128 , 1.46196328, 0.55403977],
  [ 1.60530819, 2.33479767, 2.57498862, 1.37639801],
  [ 1.04216109, 0.97715783, 1.17609438, 0.71793208]],

 [[ 0.1055839 , 0.66864782, 0.87158109, 0.36204295],
  [ 0.96613275, 1.97814629, 2.12435555, 0.97276618],
  [ 1.26778987, 1.01822369, 1.45453542, 0.45243098]]]
    )

    assert (g.shape == in_target.shape), "Wrong size"
    assert close_enough(g, in_target), "Wrong values in input gradients"
    print("     OK")

    print("Backward computation implemented ok!")


if __name__ == "__main__":
    test_convolutional_layer()
