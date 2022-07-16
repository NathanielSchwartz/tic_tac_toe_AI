def tic_tac_toe_rules(network, inputs, desired):
    cdef int times, index, output_counter, inputs_bin_len, num, inverse_index, running_cost
    cdef float costs[9]
    cdef bint valid
    outputs = [0 for i in range(9)]
    for time in range(len(inputs)):
        running_cost = 0
        output_counter = 0
        num = times + 1
        network.run(inputs, outputs, time)
        # for i in range(9):
            # costs[i] +=
        network.calc_cost(outputs, desired, running_cost, time, 'add')
        # print(running_cost)
