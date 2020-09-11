import random
from environment import TicTacToe, X, O


class Agent:
    def __init__(self, plays=X, episodes=10_000):
        """
        Initialise the agent with all the possible board states in a look up table.
        
        Winning states have a value of 1, losing states have -1. All else are 0
        """
        # initiate all possible board states
        self.plays = plays
        self.episodes = episodes
        
        self.board_states = {}
        tic_tac_toe = TicTacToe()  # blank board to test against
        
        # Get all possible states of the board (.set_board will remove duplicate permiatations)
        for board in self.fill_board([0 for x in range(9)]):
            _, winner, terminated = tic_tac_toe.eval(board)
            
            value = random.random() - 0.5
            if terminated:
                if self.plays == X:
                    if winner == X: value = 1
                    if winner == O: value = -1
                else:
                    if winner == O: value = 1
                    if winner == X: value = -1
            
            self.set_board_value(board, value)
            
        # LEARN
        self.optimise()
            
    def optimise(self):
        """
        This funciton is called to optimise it's self and learn the values of different boards
        """
        plays = {
            "X Wins!": 0,
            "Draw!": 0,
            "O Wins!": 0
        }

        print("Training")

        epsilon = 0.8
        epsilon_decay = epsilon / self.episodes
        for episode in range(1, self.episodes + 1):
            epsilon -= epsilon_decay
            ttt = TicTacToe()
            
            epsiode_moves, episode_reward = [], 0
            
            if episode % 2 == 1:
                ttt.random_step(player=-self.plays)
            
            terminated = False
            while not terminated:
                action = self.predict(ttt, epsilon)
                state, reward, terminated, info = ttt.step(action, player=self.plays)
                epsiode_moves.append(state)
                
                if terminated:
                    episode_reward = reward
                    plays[info["status"]] += 1
                    break
                    
                state, reward, terminated, info = ttt.random_step(player=-self.plays)
                if terminated:
                    plays[info["status"]] += 1
                    episode_reward = -reward
                    
            # train the results
            self.train(epsiode_moves, episode_reward)
        print("Done.")
        print(plays)

    def fill_board(self, initial_board, i=0):
        """
            This function gets all possible states of the board (with symetry)
        """
        boards = []
        if i < 9:
            x_board = [x for x in initial_board]
            o_board = [x for x in initial_board]
            b_board = [x for x in initial_board]
            x_board[i], o_board[i], b_board[i] = X, O, 0
            
            if abs(x_board.count(X) - x_board.count(O)) < 2: boards += [x_board]
            if abs(o_board.count(X) - o_board.count(O)) < 2: boards += [o_board]
            if abs(b_board.count(X) - b_board.count(O)) < 2: boards += [b_board]

            boards += self.fill_board(x_board, i+1)
            boards += self.fill_board(o_board, i+1)
            boards += self.fill_board(b_board, i+1)
        return boards

    def board_to_string(self, board):
        """
            Convert the given board to a string of the boad
        """
        board_string = ""
        for v in board:
            if v == X: board_string += "X"
            elif v == O: board_string += "O"
            else: board_string += "_"
        return board_string

    def string_to_board(self, board_string):
        """
            Convert the given string to the numeric board
        """
        board = []
        for v in board_string:
            if v == "X": board += [X]
            elif v == "O": board += [O]
            else: board += [0]
        return board

    def train(self, games_states, game_reward, lr=0.1):
        """
        Given all resulting states of game that the agent played and the reward for the
        game, the agent will train using the function temporal difference function:
            V(st) = V(st) + lr * (V(st+1) - V(st))
        """
        games_states.reverse()
        
        last_state = games_states[0]
        self.set_board_value(last_state, game_reward)
        
        for i in range(1, len(games_states)):
            current_state = games_states[i]
            
            next_value = self.get_board_value(last_state)
            current_value = self.get_board_value(current_state)
            
            new_value = current_value + lr * (next_value - current_value)
            self.set_board_value(current_state, new_value)
            
            last_state = current_state
                
    def get_board_permutations(self, board):
        """
        Given a board, this function will get all possible permiatations of the same board
        """
        permutations = []

        def flip_vert(board):
            return [board[2], board[1], board[0], board[5], board[4], board[3], board[8], board[7], board[6]]
        def flip_horz(board):
            return [board[6], board[7], board[8], board[3], board[4], board[5], board[0], board[1], board[2]]
        def flip_diag_a(board):
            return [board[0], board[3], board[6], board[1], board[4], board[7], board[2], board[5], board[8]]
        def flip_diag_b(board):
            return [board[8], board[5], board[2], board[7], board[4], board[1], board[6], board[3], board[0]]
        def rotate(board):
            return [board[6], board[3], board[0], board[7], board[4], board[1], board[8], board[5], board[2]]

        for rotation in range(4):  # for rotation
            for flipped_vert in [False, True]:
                for flipped_horz in [False, True]:
                    for flipped_diag_a in [False, True]:
                        for flipped_diag_b in [False, True]:
                            board_copy = [x for x in board]
            
                            if flipped_vert: board_copy = flip_vert(board_copy)
                            if flipped_horz: board_copy = flip_horz(board_copy)
                            if flipped_diag_a: board_copy = flip_diag_a(board_copy)
                            if flipped_diag_b: board_copy = flip_diag_b(board_copy)
                            for _ in range(rotation): board_copy = rotate(board_copy)

                            permutations += [board_copy]
        return permutations
                

    def get_board_value(self, board):
        """
            Get the value of the board
        """
        for permutations in self.get_board_permutations(board):
            board_string = self.board_to_string(permutations)
            if board_string in self.board_states:
                return self.board_states[board_string]
        return

    def set_board_value(self, board, value):
        """
        Set the value of the board
        """
        # check if it's permutation exists in the known states
        for permutations in self.get_board_permutations(board):
            board_string = self.board_to_string(permutations)
            if board_string in self.board_states:
                self.board_states[board_string] = value
                return

        self.board_states[board_string] = value
        return
        
    def predict(self, ttt, epsilon=0):
        """
        Given the environment, get all moves and compare the value of the moves
        then choose the best value. If random < epsilon then return random aciton.
        """
        possible_moves = ttt.moves(self.plays)
        action, value = 0, -2
            
        for move in possible_moves:
            future_action, board = move
            future_value = self.get_board_value(board)
            
            if future_value > value:
                action, value = future_action, future_value
        
        if random.random() < epsilon:
            action = random.choice(possible_moves)[0]

        return action
        
