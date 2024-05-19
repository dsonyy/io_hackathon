from .equations import Equation
from .random_equations import RandomEquations
from random import randint

class MathProblem:
    def __init__(self, equation: Equation, wrong_answers: list[int], blank_index: int, answer: int) -> None:
        self.wrong_answers = wrong_answers
        self.answer = answer
        self.equation = equation
        self.blank_index = blank_index

class MathProblems:
    def __getRandomAnswers(answer: int, answers_num: int):
        answers = []
        min_val = max(1, answer-10)
        max_val = min(99, answer+10)
        while len(answers) < answers_num:
            num = randint(min_val, max_val)
            if num not in answers:
                answers.append(num)

        return answers

    def getProblem(problem_index: int, wrong_answers_num: int = 4):
        match problem_index:
            case 0:
                eq = RandomEquations.getAddEquation()
            case 1:
                eq = RandomEquations.getSubEquation()
            case 2:
                eq = RandomEquations.getAddSubEquation()
            case 3:
                eq = RandomEquations.getMulEquation()
            case 4:
                eq = RandomEquations.getDivEquation()
            case 5:
                eq = RandomEquations.getMulAddEquation()
            case 6:
                eq = RandomEquations.getMulSubEquation()
        
        nums = eq.left_side.numbers
        blank_index = randint(0, len(nums)-1)
        answer = int(nums[blank_index])
        wa = MathProblems.__getRandomAnswers(answer, wrong_answers_num)
        return MathProblem(eq, wa, blank_index, answer)
    

if __name__ == "__main__":
    for i in range(7):
        p: MathProblem = MathProblems.getProblem(i, 4)
        print(p.equation, p.blank_index, p.answer, p.wrong_answers)