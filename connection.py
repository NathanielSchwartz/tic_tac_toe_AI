from neuron import Neuron


class Connection:

    def __init__(self, weight: float, output_neuron: Neuron, value: float = 0):
        self.weight = weight
        self.neuron = output_neuron
        self.value = value

    def __str__(self):
        return str(f'Value:{self.value}, Weight:{self.weight}, To:{str(self.neuron)}')

    def transmit(self):
        self.neuron.value += self.value * self.weight
        self.value = 0
