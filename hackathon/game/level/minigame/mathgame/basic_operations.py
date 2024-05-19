from enum import Enum

class BasicOperations(Enum):
    ADDITION = 1
    SUBTRACTION = 2
    DIVISION = 3
    MULTIPLICATION = 4

    def eval(self, arg1: int, arg2: int):
        match self.value:
            case self.ADDITION:
                return arg1 * arg2
            case self.SUBTRACTION:
                return arg1 - arg2
            case self.DIVISION:
                return arg1 / arg2
            case self.MULTIPLICATION:
                return arg1 * arg2

    def __str__(self):
        match self.value:
            case self.ADDITION:
                return '+'
            case self.SUBTRACTION:
                return '-'
            case self.DIVISION:
                return '/'
            case self.MULTIPLICATION:
                return '*'