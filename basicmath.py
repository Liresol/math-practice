import random
import problem
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
"""
Creates a random addition problem using numbers from min to max, inclusive
"""
#TODO: Implement settings
#TODO: And figure out what to do if settings are not there
#Figured it out: have a default config file

def update_config():
    global config
    config.read('config.ini')
    #print(config['Addition']['min'])
def addition_problem():
    min = int(config['Addition']['min'])
    max = int(config['Addition']['max'])
    add1 = random.randint(min, max)
    add2 = random.randint(min, max)
    question = str(add1) + " + " + str(add2) + " = "
    answer = add1 + add2
    return problem.Problem(question,answer, 'addition')
"""
Creates a random subtraction problem using numbers from min to max, inclusive
"""
def subtraction_problem():
    min = int(config['Subtraction']['min'])
    max = int(config['Subtraction']['max'])
    sub1 = random.randint(min, max)
    sub2 = random.randint(min, max)
    if sub1 < sub2:
        sub1 = sub2 - sub1
        sub2 = sub2 - sub1
        sub1 = sub2 + sub1
    question = str(sub1) + " - " + str(sub2) + " = "
    answer = sub1 - sub2
    return problem.Problem(question, answer, 'subtraction')
        
def multiplication_problem(min = 10, max = 100):
    min = int(config['Multiplication']['min'])
    max = int(config['Multiplication']['max'])
    mul1 = random.randint(min, max)
    mul2 = random.randint(min, max)
    question = str(mul1) + " · " + str(mul2) + " = "
    answer = mul1 * mul2
    return problem.Problem(question, answer, 'multiplication')
def integer_division_problem(min = 10, max = 100):
    min = int(config['Division']['min'])
    max = int(config['Division']['max'])
    div1 = random.randint(min, max)
    div2 = random.randint(min, max)
    question = str(div1*div2) + " / " + str(div1) + " = "
    answer = div2
    return problem.Problem(question, answer, 'int_division')
