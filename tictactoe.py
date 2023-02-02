class Board:

    def __init__(self):
        self.layout = [[Piece(False, 0) for y in range(3)] for x in range(3)]
        self.turn = 0

    def convert(self):
        converted_board = [[0] * 20]
        for x, column in enumerate(self.layout):
            for y, piece in enumerate(column):
                if piece.color == 0:
                    converted_board[0][(x * 3 + y) * 2] = 1
                    converted_board[0][(x * 3 + y) * 2 + 1] = 0
                else:
                    converted_board[0][(x * 3 + y) * 2] = 0
                    converted_board[0][(x * 3 + y) * 2 + 1] = 1

        if self.turn == 0:
            converted_board[0][18] = 1
            converted_board[0][19] = 0
        else:
            converted_board[0][18] = 0
            converted_board[0][19] = 1

        return converted_board

    def __str__(self):
        converted_board = []
        for x in self.layout:
            for y in x:
                if y.exists:
                    if y.color == 0:
                        converted_board.append('X')
                    else:
                        converted_board.append('O')
                else:
                    converted_board.append(' ')
        if self.turn == 0:
            player = 'X'
        else:
            player = 'O'
        return str(f'--{player}--\n{converted_board[0]} {converted_board[1]} {converted_board[2]}\n{converted_board[3]}'
                   f' {converted_board[4]} {converted_board[5]}\n{converted_board[6]} {converted_board[7]}'
                   f' {converted_board[8]}\n-----')


class Piece:

    def __init__(self, exists, color):
        self.exists = exists
        self.color = color


class Move:

    def __init__(self, num=0, value=0):
        self.num = num
        self.value = value

    def __add__(self, other):
        return Move(self.num + other.num, self.value + other.value)
