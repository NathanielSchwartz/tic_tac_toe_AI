import math


class Neuron:

    def __init__(self, logistic_growth_rate: float, sigmoid_midpoint: float,
                 connections: list, value: float = 0):
        self.rate = logistic_growth_rate
        self.midpoint = sigmoid_midpoint
        self.connections = connections
        self.value = value

    def __str__(self):
        return str(f'Value:{self.value}, Growth Rate:{self.rate}, Midpoint:{self.midpoint} '
                   f'Connections:{len(self.connections)}')

    def transmit(self):
        exponent = -self.rate * (self.value + self.midpoint)
        if exponent >= 100:
            self.value = 0.0
        elif exponent <= -100:
            self.value = 1.0
        else:
            self.value = 1 / (1 + math.e ** exponent)
        for connection in self.connections:
            connection.value = self.value
        self.value = 0
