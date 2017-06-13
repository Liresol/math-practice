from abc import ABC, abstractmethod

"""
"""
class Problem:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.answered = False
        self.correct = False
    def evaluate_answer(self, answer):
        if answer == self.answer and not self.answered:
            self.correct = True

        if type(answer) is str and type(self.answer) is int:
            answer = int(answer)
            if answer == self.answer and not self.answered:
                self.correct = True
        self.answered = True
