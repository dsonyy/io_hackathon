from .equations import Equation, EquationSide
from .basic_operations import BasicOperation
from random import randint


class RandomEquations:
    def getAddEquation():
        sum = RandomEquations.__getRandomNotZeroValue(2, 99)
        num1 = RandomEquations.__getRandomNotZeroValue(1, sum-1)
        num2 = sum - num1
        left = EquationSide()
        left.add_number(num1)
        left.add_operation(BasicOperation.ADDITION)
        left.add_number(num2)
        eq = Equation(left, sum)
        return eq

    def getSubEquation():
        num1 = RandomEquations.__getRandomNotZeroValue(2, 99)
        diff = RandomEquations.__getRandomNotZeroValue(1, num1-1)
        num2 = num1 - diff
        left = EquationSide()
        left.add_number(num1)
        left.add_operation(BasicOperation.SUBTRACTION)
        left.add_number(num2)
        eq = Equation(left, diff)
        return eq

    def getAddSubEquation():
        add_first = randint(0, 1)
        if add_first:
            add_eq = RandomEquations.getAddEquation()
            
            num1 = add_eq.right_side
            diff = RandomEquations.__getRandomNotZeroValue(1, num1-1)
            num2 = num1 - diff
            left = add_eq.left_side
            left.add_operation(BasicOperation.SUBTRACTION)
            left.add_number(num2)
            eq = Equation(left, diff)
            return eq
        else:
            sub_eq = RandomEquations.getSubEquation()
            sum = RandomEquations.__getRandomNotZeroValue(sub_eq.right_side+1, 99)
            num1 = sub_eq.right_side
            num2 = sum - num1
            left = sub_eq.left_side
            left.add_operation(BasicOperation.ADDITION)
            left.add_number(num2)
            eq = Equation(left, sum)
            return eq
        

    def getMulEquation():
        num1 = RandomEquations.__getRandomNotZeroValue(2, 49)
        num2 = RandomEquations.__getRandomNotZeroValue(min(98, 2*num1), 98) // num1
        swap_nums = randint(0, 1)
        if swap_nums:
            num1, num2 = num2, num1
        prod = num1 * num2
        left = EquationSide()
        left.add_number(num1)
        left.add_operation(BasicOperation.MULTIPLICATION)
        left.add_number(num2)
        eq = Equation(left, prod)
        return eq

    def getDivEquation():
        quo = RandomEquations.__getRandomNotZeroValue(2, 49)
        num2 = RandomEquations.__getRandomNotZeroValue(min(98, 2*quo), 98) // quo
        swap_nums = randint(0, 1)
        if swap_nums:
            quo, num2 = num2, quo
        num1 = quo * num2
        left = EquationSide()
        left.add_number(num1)
        left.add_operation(BasicOperation.DIVISION)
        left.add_number(num2)
        eq = Equation(left, quo)
        return eq

    def getMulAddEquation():
        mul_eq = RandomEquations.getMulEquation()
    
        mul_first = randint(0, 1)
        sum = RandomEquations.__getRandomNotZeroValue(mul_eq.right_side+1, 99)
        num1 = mul_eq.right_side
        num2 = sum - num1
        if mul_first:
            left = mul_eq.left_side
            left.add_operation(BasicOperation.ADDITION)
            left.add_number(num2)
        else:
            left = EquationSide()
            left.add_number(num2)
            left.add_operation(BasicOperation.ADDITION)
            left.add_number(mul_eq.left_side.numbers[0])
            left.add_operation(BasicOperation.MULTIPLICATION)
            left.add_number(mul_eq.left_side.numbers[1])

        eq = Equation(left, sum)
        return eq

    def getMulSubEquation():
        mul_eq = RandomEquations.getMulEquation()
        num1 = mul_eq.right_side
        diff = RandomEquations.__getRandomNotZeroValue(1, num1-1)
        num2 = num1 - diff

        left = mul_eq.left_side
        left.add_operation(BasicOperation.SUBTRACTION)
        left.add_number(num2)
        eq = Equation(left, diff)
        return eq

    # def getDivAddEquation():
    #     pass

    # def getDivSubEquation():
    #     pass

    def __getRandomNotZeroValue(min_val: int, max_val: int) -> int:
        while min_val < max_val:
            num = randint(min_val, max_val)
            if num != 0:
                return num
        return min_val


if __name__ == "__main__":
    eq = RandomEquations.getAddEquation()
    print(eq)

    eq = RandomEquations.getSubEquation()
    print(eq)

    eq = RandomEquations.getAddSubEquation()
    print(eq)

    eq = RandomEquations.getMulEquation()
    print(eq)

    eq = RandomEquations.getDivEquation()
    print(eq)

    eq = RandomEquations.getMulAddEquation()
    print(eq)

    eq = RandomEquations.getMulSubEquation()
    print(eq)