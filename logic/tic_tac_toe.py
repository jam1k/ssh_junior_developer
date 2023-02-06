# tic_tac_toe/logic/tic_tac_toe.py

import random
import time

from validators import get_winner, get_starting_mark, get_mark_other, validate_game_state

def possibilities(grid: str):
    """From the input grid as string find indexes of all empty cells(equal to '-')"""
    l = []
    for i in range(len(grid)):
        if grid[i] == "-":
            l.append(i)
    return l

def random_place(grid: str, mark:str):
    """Select a place to put X or O"""
    resulting_grid = []
    selection = possibilities(grid)
    if len(selection) != 0:
        current_loc = random.choice(selection)
        resulting_grid = grid[:current_loc] + mark + grid[current_loc + 1:]
    else:
        return None
    return resulting_grid
    

def play_game(board: str):
    """This function was developed for testing purposes.
    The function emaluates the game of two computers"""
    player1 = get_starting_mark(board)
    player2 = get_mark_other(player1)
    counter = 1
    print(board)
    
    winner = None
    while winner == None and bool(board):
        for player in [player2, player1]:
            board = random_place(board, player)
            if bool(board) == False:
                break 
            print("Board after " + str(counter) + " move")
            print(board)
            time.sleep(1)
            counter += 1
            winner = get_winner(board)
            if winner != None:
                break
    return(winner)


def play_game_backend(game: dict):
    """Main game loop with moves"""
    winner = get_winner(game["board"])
    if winner != None:
        game["status"] = "FINISHED"
        game["winner"] = winner
        return game

    try: 
        validate_game_state(game["board"], game["starting_mark"])
    except:
        raise
    
    board = random_place(game["board"], game["computer_mark"])
    
    if board == None:
        game["status"] = "FINISHED"
        game["winner"] = "Tie"
    else:
        game["board"] = board

    winner = get_winner(board)

    if winner != None:
        game["status"] = "FINISHED"
        game["winner"] = winner
    try: 
        validate_game_state(board, game["starting_mark"])
    except:
        raise

    reamining_possibilities = possibilities(game["board"])
    if len(reamining_possibilities) == 0:
        game["status"] = "FINISHED"
        game["winner"] = "Tie"
    return game 

# Required for testing
if __name__ == "__main__":
    print(f"The winner is {play_game('--------')}")