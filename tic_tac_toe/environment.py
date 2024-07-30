import random

X = 1
O = -1


class TicTacToe:
    def __init__(self):
        self.board = [0 for _ in range(9)]

    def eval(self, board=None):
        """
        Evaluates the current board state (or given board).
            
        :return: board_state, the winning player (or 0), and if the game is terminated
        """
        if board is None: board = self.board

        def eval_cols(value):
            return sum(board[0:9:3]) == (value * 3) or sum(board[1:9:3]) == (value * 3) or sum(board[2:9:3]) == (value * 3)

        def eval_rows(value):
            return sum(board[0:3]) == (value * 3) or sum(board[3:6]) == (value * 3) or sum(board[6:9]) == (value * 3)

        def eval_diags(value):
            return (sum(board[0:9:4]) == (value * 3)) or (sum(board[2:7:2]) == (value * 3))

        if eval_cols(O) or eval_rows(O) or eval_diags(O):
            return [x for x in board], O, True

        if eval_rows(X) or eval_cols(X) or eval_diags(X):
            return [x for x in board], X, True

        if 0 not in board:
            return [x for x in board], 0, True
        return [x for x in board], 0, False

    def step(self, index, player=0):
        if self.board[index] == 0:
            self.board[index] = player
        else:
            raise Exception(f"Non-zero position at index {index}.")
        
        reward = 0
        state, winner, terminated = self.eval(board=self.board)
        info = {"status": "Draw!"}
        if terminated:
            if winner == player: reward = 1
            if winner == X: info["status"] = "X Wins!"
            if winner == O: info["status"] = "O Wins!"
        return state, reward, terminated, info
        
    def random_step(self, player=0):
        index = random.choice(self.moves(player=player))[0]
        return self.step(index, player=player)
        
    def moves(self, player=0, board=None):
        _board = board
        if _board is None: _board = self.board
    
        moves = []
        for index in range(len(_board)):
            if _board[index] == 0:
                new_board = [x for x in _board]
                new_board[index] = player
                moves.append((index, new_board))

        return moves

    def render(self):
        data = "  {}  |  {}  |  {}  "
        row = "     |     |     "
        space = "-----+-----+-----"
        
        def val(x):
            if x == -1: return "O"
            if x == 1: return "X"
            return " "
        
        print("\n".join([
            "",
            row,
            data.format(val(self.board[0]), val(self.board[1]), val(self.board[2])),
            row,
            space,
            row,
            data.format(val(self.board[3]), val(self.board[4]), val(self.board[5])),
            row,
            space,
            row,
            data.format(val(self.board[6]), val(self.board[7]), val(self.board[8])),
            row,
            ""
        ]))
