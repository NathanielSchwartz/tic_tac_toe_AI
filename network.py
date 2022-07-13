import random
import math
import copy
from neuron import Neuron
from connection import Connection


class Network:

    def __init__(self, input_neuron_number: int, hidden_neuron_number: int, hidden_layer_number: int,
                 output_neuron_number: int,
                 input_neuron_list=None, hidden_neuron_list=None, output_neuron_list=None, cost: float = 0):
        self.in_num = input_neuron_number
        self.hn_num = hidden_neuron_number
        self.hn_lay = hidden_layer_number
        self.on_num = output_neuron_number
        self.cost = cost
        if input_neuron_list is None:
            self.in_list = []
        else:
            self.in_list = input_neuron_list.copy()
        if hidden_neuron_list is None:
            self.hn_list = []
        else:
            self.hn_list = hidden_neuron_list.copy()
        if output_neuron_list is None:
            self.on_list = []
        else:
            self.on_list = output_neuron_list.copy()

    def __str__(self):
        return str(f'Inputs:{self.in_num} Hiddens:{self.hn_num} in {self.hn_lay} layer(s). Outputs:{self.on_num} '
                   f'Cost:{self.cost}')

    def generate(self):
        for i in range(self.in_num):
            self.in_list.append(Neuron(0, 0, []))
        for i in range(self.on_num):
            self.on_list.append(Neuron(0, 0, []))
        for i in range(self.hn_lay):
            self.hn_list.append([])
            for j in range(self.hn_num):
                self.hn_list[i].append(Neuron(0, 0, []))
        if self.hn_list is not []:
            for i in self.in_list:
                for j in self.hn_list[0]:
                    i.connections.append(Connection(0, j))
            for index, layer in enumerate(self.hn_list[:len(self.hn_list) - 1]):
                for i in layer:
                    for j in self.hn_list[index+1]:
                        i.connections.append(Connection(0, j))
            for i in self.hn_list[len(self.hn_list) - 1]:
                for j in self.on_list:
                    i.connections.append(Connection(0, j))

    def input(self, input_value_list: list):
        for index, neuron in enumerate(self.in_list):
            neuron.value = input_value_list[index]

    def output(self, output_value_list: list):
        for index, neuron in enumerate(self.on_list):
            exponent = -neuron.rate * (neuron.value + neuron.midpoint)
            if exponent >= 100:
                neuron.value = 0.0
            elif exponent <= -100:
                neuron.value = 1.0
            else:
                neuron.value = 1 / (1 + math.pow(math.e, exponent))
            output_value_list[index] = neuron.value
            neuron.value = 0

    def run(self, input_value_list: list, output_value_list: list):
        self.input(input_value_list)
        [neuron.transmit() for neuron in self.in_list]
        [[connection.transmit() for connection in neuron.connections] for neuron in self.in_list]
        for layer in self.hn_list:
            [neuron.transmit() for neuron in layer]
            [[connection.transmit() for connection in neuron.connections] for neuron in layer]
        self.output(output_value_list)

    def mutate(self, m_rate: float = 1.0):
        self.cost = 0
        for i in self.in_list:
            i.rate += random.uniform(-m_rate, m_rate)
            i.midpoint += random.uniform(-m_rate, m_rate)
        for i in self.on_list:
            i.rate += random.uniform(-m_rate, m_rate)
            i.midpoint += random.uniform(-m_rate, m_rate)
        for i in self.hn_list:
            for j in i:
                j.rate += random.uniform(-m_rate, m_rate)
                j.midpoint += random.uniform(-m_rate, m_rate)
        if self.hn_list is not []:
            for i in self.in_list:
                for index, j in enumerate(self.hn_list[0]):
                    i.connections[index].weight += random.uniform(-m_rate, m_rate)
                    i.connections[index].neuron = j
            for index, layer in enumerate(self.hn_list[:len(self.hn_list) - 1]):
                for i in layer:
                    for index2, j in enumerate(self.hn_list[index+1]):
                        i.connections[index2].weight += random.uniform(-m_rate, m_rate)
                        i.connections[index2].neuron = j
            for i in self.hn_list[len(self.hn_list) - 1]:
                for index, j in enumerate(self.on_list):
                    i.connections[index].weight += random.uniform(-m_rate, m_rate)
                    i.connections[index].neuron = j

    def calc_cost(self, output_value_list: list, desired_value_list: list, mode: str = 'rewrite'):
        if mode == 'rewrite':
            self.cost = 0
        for index, value in enumerate(output_value_list):
            self.cost += abs(desired_value_list[index] - value)

    def copy(self):
        return copy.deepcopy(self)
