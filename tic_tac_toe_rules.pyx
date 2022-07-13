def tic_tac_toe_rules(network):
    cdef int times, index, output_counter, inputs_bin_len, num, inverse_index
    cdef int inputs[18]
    cdef int desired[9]
    cdef bint valid
    outputs = [0 for i in range(9)]
    for times in range(2 ** 18):
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
            network.calc_cost(outputs, list_desired, 'add')
