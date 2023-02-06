# tic_tac_toe/logic/validators.py

import re
from cerberus import Validator
from exceptions import InvalidGameState

WINNING_PATTERNS = (
    "???......",
    "...???...",
    "......???",
    "?..?..?..",
    ".?..?..?.",
    "..?..?..?",
    "?...?...?",
    "..?.?.?..",
)

def validate_board(bord_dict: dict):
    schema = {
        'board': {'type': 'string', 'empty': False, 'regex': '[OX-]+', 'minlength': 9, 'maxlength': 9}
        }
    v = Validator(schema)
    v.validate(bord_dict)
    if bool(v.errors):
        raise InvalidGameState(v.errors["board"][0])
    

def check_initial_grid(grid: str):
    """The function checks that initial grid has all empty cells or only one X or O move"""
    x_count = get_x_count(grid)
    o_count = get_o_count(grid)
   
    if x_count > 1:
        raise InvalidGameState("Initial board should have all - or one X move")
        
    elif o_count > 1:
        raise InvalidGameState("Initial board should have all - or one O move")
        
    elif x_count == 1 and o_count == 1:
        raise InvalidGameState("Initial board should have all either one X or one Y")


def get_x_count(grid):
    """The function returns the count of X chars"""
    return grid.count("X")


def get_o_count(grid):
    """The function returns the count of O chars"""
    return grid.count("O")


def get_empty_count(grid):
    """The function returns the count of empty cells"""
    return grid.count("-")


def get_starting_mark(grid: str):
    """The function returns the starting mark selected by the player.
    If starting mark is O, returns O, else return default starting mark X"""
    x_count = get_x_count(grid)
    o_count = get_o_count(grid)
    if x_count == 1:
        return "X"
    elif o_count == 1:
        return "O"
    else:
        return "X"


def get_mark_other(player1_mark: str):
    """The function return other mark which diifers from initial. Default is X"""
    if player1_mark == "X":
        return "O"
    else:
        return "X"


def get_winner(grid):
    """The function checks if there is a winner."""
    marks = ["X", "O"]
    for pattern in WINNING_PATTERNS:
        for mark in marks:
                if re.match(pattern.replace("?", mark), grid):
                    return mark
    return None


def validate_game_state(grid: str, starting_mark: str):
    
    try:
        validate_number_of_marks(grid)
        validate_starting_mark(grid, starting_mark)
        winner = get_winner(grid)
        validate_winner(grid, starting_mark, winner)
    except:
        raise

def validate_number_of_marks(grid: str):
    x_count = get_x_count(grid)
    o_count = get_o_count(grid)
    
    if abs(x_count - o_count) > 1:
        raise InvalidGameState("Wrong number of Xs and Os")

def validate_starting_mark(grid: str, starting_mark: str):
    x_count = get_x_count(grid)
    o_count = get_o_count(grid)
    if x_count > o_count:
        if starting_mark != "X":
            raise InvalidGameState("Check the mark(Os/Xs), it is probably the other player turn")
    elif o_count > x_count:
        if starting_mark != "O":
            raise InvalidGameState("Check the mark(Os/Xs), it is probably the other player turn")
    

def validate_winner(grid: str, starting_mark: str, winner: str | None) -> None:
    x_count = get_x_count(grid)
    o_count = get_o_count(grid)
    if winner == "X":
        if starting_mark == "X":
            if x_count <= o_count:
                raise InvalidGameState("Input grid contains less Xs then expected. X can win only when number of Xs more than number of Os")
        else:
            if x_count != o_count:
                raise InvalidGameState("Input grid contains less Xs then expected. X can win only when number of Xs more than number of Os")
    elif winner == "O":
        if starting_mark == "O":
            if o_count <=  x_count:
                raise InvalidGameState("Input grid contains less Os then expected. O can win only when number of Os more than number of Xs")
        else:
            if o_count !=  x_count:
                raise InvalidGameState("Input grid contains less Os then expected. O can win only when number of Os more than number of Xs")


def validate_difference_1char_allowed(game_state_str: str, put_str: str):
    """The function checks that two input strings differs only by one char"""
    ok = False

    for c1, c2 in zip(game_state_str, put_str):
        if c1 != c2:
            if ok:
                raise InvalidGameState("Check the input board. Does not correspond to the gamestate")
            else:
                ok = True
    return True

if __name__ == "__main__":
    print(validate_difference_1char_allowed("-OOX", "---X"))