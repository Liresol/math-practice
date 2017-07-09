"""
Problem class. Contains a question, an answer, and a
question category.
"""
class Problem:
    def __init__(self, question, answer, category):
        self.question = question
        self.answer = answer
        self.answered = False
        self.correct = False
        self.category = category
    def evaluate_answer(self, answer):
        if not self.answered:
            if type(answer) is str and type(self.answer) is int:
                try:
                    answer = int(answer)
                    if answer == self.answer:
                        self.correct = True
                except ValueError:
                    pass
            if answer == self.answer:
                self.correct = True
        self.answered = True
