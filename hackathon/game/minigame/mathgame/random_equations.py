from random import randint
from equations import Equation, EquationSide
from basic_operations import BasicOperation


class RandomEquations:
    def getOneAddEquation():
        sum = RandomEquations.__getRandomNotZeroValue(2, 99)
        num1 = RandomEquations.__getRandomNotZeroValue(1, sum-1)
        num2 = sum - num1
        left = EquationSide()
        left.add_number(str(num1))
        left.add_operation(BasicOperation.ADDITION)
        left.add_number(str(num2))
        eq = Equation(left, sum)
        return eq

    def getOneSubEquation():
        sum = RandomEquations.__getRandomNotZeroValue(2, 99)
        num1 = RandomEquations.__getRandomNotZeroValue(1, sum-1)
        num2 = sum - num1
        left = EquationSide()
        left.add_number(str(sum))
        left.add_operation(BasicOperation.SUBTRACTION)
        left.add_number(str(num2))
        eq = Equation(left, num1)
        return eq

    def getAddSubEquation():
        pass

    def getOneMulEquation():
        pass

    def getOneDivEquation():
        pass

    def getMulDivEquation():
        pass

    def __getRandomNotZeroValue(min_val: int, max_val: int) -> int:
        while min_val != max_val:
            num = randint(min_val, max_val)
            if num != 0:
                return num
        return min_val


if __name__ == "__main__":
    eq = RandomEquations.getOneAddEquation()
    print(eq)

    eq = RandomEquations.getOneSubEquation()
    print(eq)