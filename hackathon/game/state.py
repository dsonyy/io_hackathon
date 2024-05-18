from enum import IntEnum, auto


class State(IntEnum):
    '''
    An enum represending game state.
    Use in main game class to handle logic and display properly.
    Add all possible screens here.
    '''

    Menu = auto()
    World = auto()
    MinigameMath = auto()
    MinigameAlgo = auto()
    MinigameElectro = auto()
