import network as net
import tictactoe as ttt
import random as rnd


# Setup
engine = net.Network([[0, 1] for i in range(20)], [15, 15, 9], 'net')

for cycle in range(10):
    # Setup per cycle
    inp_data = []
    target_data = []
    choices = [i for i in range(9)]
    training_data = {}
    engine.file = f'engine{cycle}.net'
    for game in range(1000):
        # Setup per game
        board = ttt.Board()
        playing = True
        winner = None
        temp_moves_x = {}
        temp_moves_o = {}
        while playing:
            # Setup per turn
            inputs = board.convert()
            outputs = engine.run(inputs).tolist()
            cum_sum = 0
            min_value = min(outputs[0])

            # Selecting choice
            for index, value in enumerate(outputs[0]):
                if board.layout[int(index // 3)][int(index - index // 3 * 3)].exists:
                    outputs[0][index] = 0
                else:
                    outputs[0][index] -= min_value - 0.001
                cum_sum += outputs[0][index]
            for index, value in enumerate(outputs[0]):
                outputs[0][index] /= cum_sum
            choice = rnd.choices(choices, k=1, weights=outputs[0])[0]
            x = int(choice - choice // 3 * 3)
            y = int(choice // 3)

            # Updating temp moves
            key = ''
            for i in inputs[0]:
                key += str(i)
            if board.turn == 0:
                if key not in temp_moves_x.keys():
                    temp_moves_x[key] = []
                    for i in outputs[0]:
                        temp_moves_x[key].append(ttt.Move(1, 0.5))
                temp_moves_x[key][choice] += ttt.Move(1, 0)
            else:
                if str(inputs) not in temp_moves_o.keys():
                    temp_moves_o[key] = []
                    for i in outputs[0]:
                        temp_moves_o[key].append(ttt.Move(1, 0.5))
                temp_moves_o[key][choice] += ttt.Move(1, 0)

            # Updating game board
            board.layout[y][x].exists = True
            board.layout[y][x].color = board.turn

            # Checking if game over
            if board.layout[0][x].exists and board.layout[1][x].exists and board.layout[2][x].exists:
                if board.layout[0][x].color == board.turn and board.layout[1][x].color == board.turn and \
                        board.layout[2][x].color == board.turn:
                    playing = False
                    winner = board.turn
            if board.layout[y][0].exists and board.layout[y][1].exists and board.layout[y][2].exists:
                if board.layout[y][0].color == board.turn and board.layout[y][1].color == board.turn and \
                        board.layout[y][2].color == board.turn:
                    playing = False
                    winner = board.turn
            if (x + y) % 2 == 0:
                if board.layout[0][0].exists and board.layout[1][1].exists and board.layout[2][2].exists:
                    if board.layout[0][0].color == board.turn and board.layout[1][1].color == board.turn and \
                            board.layout[2][2].color == board.turn:
                        playing = False
                        winner = board.turn
                if board.layout[2][0].exists and board.layout[1][1].exists and board.layout[0][2].exists:
                    if board.layout[2][0].color == board.turn and board.layout[1][1].color == board.turn and \
                            board.layout[0][2].color == board.turn:
                        playing = False
                        winner = board.turn
            filled = True
            for i in board.layout:
                for j in i:
                    if not j.exists:
                        filled = False
                        break
            if filled:
                playing = False
                winner = 0.5

            # Displaying final game of cycle
            if game == 999:
                print(str(board))

            # Switching turn
            if board.turn == 0:
                board.turn = 1
            else:
                board.turn = 0

        # Updating values for temp moves
        if winner == 0:
            for key in temp_moves_x:
                for i in temp_moves_x[key]:
                    i.value += i.num
        elif winner == 1:
            for key in temp_moves_o:
                for i in temp_moves_o[key]:
                    i.value += i.num
        elif winner == 0.5:
            for key in temp_moves_x:
                for i in temp_moves_x[key]:
                    i.value += i.num * 0.5
            for key in temp_moves_o:
                for i in temp_moves_o[key]:
                    i.value += i.num * 0.5

        for key in temp_moves_x.keys():
            if key not in training_data.keys():
                training_data[key] = temp_moves_x[key]
            else:
                for index, move in enumerate(temp_moves_x[key]):
                    training_data[key][index] += temp_moves_x[key][index]
        for key in temp_moves_o.keys():
            if key not in training_data.keys():
                training_data[key] = temp_moves_o[key]
            else:
                for index, move in enumerate(temp_moves_o[key]):
                    training_data[key][index] += temp_moves_o[key][index]

    # Training the Neural Network
    inputs = []
    targets = []
    for key in training_data:
        inputs.append(list(key))
        temp_targets = []
        for i in training_data[key]:
            temp_targets.append(i.value / i.num)
        targets.append(temp_targets)
    engine.train(inputs, targets)
