import math
from datetime import datetime
from tic_tac_toe_rules import tic_tac_toe_rules
from network import Network

file_read = open('best_network', mode='r')
file_write = open('best_network', mode='w')
if file_read.read() != '':
    brain1 = file_read.read()
else:
    brain1 = Network(18, 1, 1, 9)
    brain1.generate()
    tic_tac_toe_rules(brain1)
    # file_write.write(brain1)
count = 0
tries = 1
lowest = math.inf
accuracy = 1
while accuracy < 99 and count < 1000 and tries < 1000:
    start = datetime.now()
    count += 1
    brain2 = brain1.copy()
    brain2.mutate((100 - accuracy) / 100)
    tic_tac_toe_rules(brain2)
    if brain2.cost < brain1.cost:
        brain1 = brain2.copy()
        tries = 1
    else:
        tries += 1
    if brain1.cost < lowest:
        lowest = brain1.cost
        accuracy = (brain1.on_num * math.pow(3, 9) - lowest) /\
                   (brain1.on_num * math.pow(3, 9)) * 100
        # file_write.write(brain1)
        print(f'lowest cost:{lowest}, accuracy:{round(accuracy, 2)}')
    print(f'Generation Count: {count}. Time: {datetime.now() - start}. Accuracy: {round(accuracy, 2)}')
if accuracy >= 99:
    print(f'SUCCESS:{count}')
    print(f'lowest cost:{lowest}, accuracy:{round(accuracy, 2)}')
else:
    print('FAILURE')
    print(f'lowest cost:{lowest}, accuracy:{round(accuracy, 2)}')
