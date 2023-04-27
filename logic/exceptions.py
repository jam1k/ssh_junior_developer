# tic_tac_toe/logic/exceptions.py

class InvalidGameState(Exception):
    """Raised when the game state is invalid."""

    def __init__(self, error: str):
        self.error = error
        super().__init__()
