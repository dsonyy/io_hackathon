from enum import Enum

class BasicOperation(Enum):
    ADDITION = 1
    SUBTRACTION = 2
    DIVISION = 3
    MULTIPLICATION = 4

    def eval(self, arg1: int, arg2: int):
        match self:
            case BasicOperation.ADDITION:
                return arg1 + arg2
            case BasicOperation.SUBTRACTION:
                return arg1 - arg2
            case BasicOperation.DIVISION:
                if arg2 == 0:
                    raise ValueError('Division by zero is not allowed')
                return arg1 / arg2
            case BasicOperation.MULTIPLICATION:
                return arg1 * arg2

    def __str__(self):
        match self:
            case BasicOperation.ADDITION:
                return '+'
            case BasicOperation.SUBTRACTION:
                return '-'
            case BasicOperation.DIVISION:
                return '/'
            case BasicOperation.MULTIPLICATION:
                return '*'
            case _:
                return 'Unknown Operation'


if __name__ == '__main__':
    operation = BasicOperation.ADDITION
    print(f"{operation} result: {operation.eval(10, 5)}")
