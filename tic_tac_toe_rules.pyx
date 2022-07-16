def tic_tac_toe_rules(network):
    cdef int times, index, output_counter, inputs_bin_len, num, inverse_index, running_cost
    cdef int inputs[18]
    cdef int desired[9]
    cdef float costs[9]
    cdef bint valid
    for i in range(9):
        costs[i] = 0.0
    outputs = [0 for i in range(9)]
    for times in range(2 ** 18):
        running_cost = 0
        output_counter = 0
        valid = True
        num = times + 1
        for index in range(18):
            inverse_index = abs(index - 17)
            if num >= 2 ** inverse_index:
                inputs[index] = 1
                num -= 2 ** inverse_index
            else:
                inputs[index] = 0
        for index in range(0, 18, 2):
            if inputs[index] == 1 and inputs[index + 1] == 1:
                valid = False
                break
            else:
                if inputs[index] == 1 or inputs[index + 1] == 1:
                    desired[output_counter] = 0
                else:
                    desired[output_counter] = 1
            output_counter += 1
        if valid:
            list_inputs = [i for i in inputs[:18]]
            list_desired = [i for i in desired[:9]]
            network.run(list_inputs, outputs)
            # for i in range(9):
                # costs[i] +=
            network.calc_cost(outputs, list_desired, running_cost, 'add')
            # print(running_cost)
    print(costs)
    print(network.cost)
