import random
import problem
"""
Creates a random addition problem using numbers from min to max, inclusive
"""
#TODO: Implement settings
#Why are these classes
def addition_problem(min = 10, max = 100):
    add1 = random.randint(min, max)
    add2 = random.randint(min, max)
    question = str(add1) + " + " + str(add2) + " = "
    answer = add1 + add2
    return problem.Problem(question,answer)
def subtraction_problem(min = 10, max = 100):
    sub1 = random.randint(min, max)
    sub2 = random.randint(min, max)
    if sub1 < sub2:
        sub1 = sub2 - sub1
        sub2 = sub2 - sub1
        sub1 = sub2 + sub1
    question = str(sub1) + " - " + str(sub2) + " = "
    answer = sub1 - sub2
    return problem.Problem(question, answer)
        
def multiplication_problem(min = 10, max = 100):
    mul1 = random.randint(min, max)
    mul2 = random.randint(min, max)
    question = str(mul1) + " · " + str(mul2) + " = "
    answer = mul1 * mul2
    return problem.Problem(question, answer)
def integer_division_problem(min = 10, max = 100):
    div1 = random.randint(min, max)
    div2 = random.randint(min, max)
    question = str(div1*div2) + " / " + str(div1) + " = "
    answer = div2
    return problem.Problem(question, answer)
