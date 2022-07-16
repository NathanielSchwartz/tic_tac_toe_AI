import math
import random
from datetime import datetime
from tic_tac_toe_rules import tic_tac_toe_rules
from network import Network


def create_random_inputs(sample_num):
    for i in range(sample_num):
        inputs.append([])
        desired.append([])
        for j in range(9):
            square_info = random.randint(0, 2)
            pairing = bin(square_info)[2:]
            if len(pairing) == 1:
                pairing = '0' + pairing
            inputs[i].append(pairing[0])
            inputs[i].append(pairing[1])
            if pairing.count('1') == 0:
                desired[i].append(1)
            else:
                desired[i].append(0)


sample_size = 400
inputs = []
desired = []
create_random_inputs(sample_size)

file_read = open('best_network', mode='r')
file_write = open('best_network', mode='w')
if file_read.read() != '':
    brain1 = file_read.read()
else:
    brain1 = Network(18, 18, 1, 9)
    brain1.generate()
    tic_tac_toe_rules(brain1, inputs, desired)
    # file_write.write(brain1)
count = 0
tries = 1
lowest = math.inf
accuracy = 1
while accuracy < 99 and count < 1000000 and tries < 100000:
    start = datetime.now()
    count += 1
    brain2 = brain1.copy()
    brain2.mutate((100 - accuracy) / 50)
    tic_tac_toe_rules(brain2, inputs, desired)
    if brain2.cost < brain1.cost:
        brain1 = brain2.copy()
        tries = 1
    else:
        tries += 1
    if brain1.cost < lowest:
        lowest = brain1.cost
        accuracy = (sample_size - lowest) / sample_size * 100
        # file_write.write(brain1)
    print(f'Lowest cost:{lowest}, Accuracy:{round(accuracy, 3)}')
    print(f'Generation Count: {count}, Time: {datetime.now() - start}\n')
if accuracy >= 99:
    print(f'SUCCESS:{count}')
    print(f'lowest cost:{lowest}, accuracy:{round(accuracy, 3)}')
else:
    print('FAILURE')
    print(f'lowest cost:{lowest}, accuracy:{round(accuracy, 3)}')
