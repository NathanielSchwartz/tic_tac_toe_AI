import neurolab as nl


class Network:

    def __init__(self, input_ranges, layers, file='engine.net'):
        self.net = nl.net.newff(input_ranges, layers)
        self.file = file
        self.net.trainf = nl.train.train_gd

    def train(self, inp_data, target_data):
        error = self.net.train(inp_data, target_data, lr=0.00001, epochs=7200)
        self.net.save(self.file)
        return error

    def run(self, inp_data):
        output = self.net.sim(inp_data)
        return output
