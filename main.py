import random
from environment import TicTacToe, X, O
from agent import Agent

        
def get_player_move(env):
    """
    Get the player move as an index in the board
    """
    valid_moves = ["a1", "a2", "a3", "b1", "b2", "b3", "c1", "c2", "c3"]
    while True:
        move = input("Where would you like to go? (a2, b1, c3, ...): ")
        if move in valid_moves:
            return valid_moves.index(move)
        else:
            print("Invalid move: " + move)


comp = X
human = O

agent = Agent(plays=comp, episodes=10_000)

if __name__ == "__main__":
    playing = True
    while playing:
        env = TicTacToe()  # initialise game
        env.render()

        # if user does not go first then the agent makes a prediction
        if input("Would you like to go first? (yes/no): ").lower() != "yes":
            action = agent.predict(env)
            env.step(action, player=comp)
            env.render()

        game_over = False
        while not game_over:
            # human move
            index = get_player_move(env)
            step, reward, game_over, result = env.step(index, player=human)
            env.render()
            
            if not game_over:
                # ai move
                action = agent.predict(env)
                _, _, game_over, result = env.step(action, player=comp)
                env.render()
                    
            if game_over:
                print(result["status"])
                play_again = input("Would you like to play again? (yes/no): ")
                if play_again.lower() != "yes":
                    playing = False
