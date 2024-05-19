from .basic_operations import BasicOperation

class EquationSide:
        def __init__(self) -> None:
            self.numbers: list[int] = []
            self.operations: list[BasicOperation] = []

        def add_number(self, num: int):
            self.numbers.append(num)
        
        def add_operation(self, operation: BasicOperation):
            self.operations.append(operation)

        def __str__(self):
            el = []
            el.append(str(self.numbers[0]))
            for i in range(len(self.numbers)-1):
                el.append(str(self.operations[i]))
                el.append(str(self.numbers[i+1]))
            return ' '.join(el)

class Equation:
    def __init__(self, left_side: EquationSide, right_side: int) -> None:
        self.left_side = left_side
        self.right_side = right_side

    def __str__(self) -> str:
        el = []
        el.append(str(self.left_side))
        el.append("=") 
        el.append(str(self.right_side))
        return ' '.join(el)