from constants import TOKEN_ADD, TOKEN_SUB, TOKEN_MUL, TOKEN_DIV
from _parser.parser import identifiers

class Expression(object):
    def evaluate(self):
        return None

class IdentifierExpression(Expression):
    def __init__(self, id):
        self.id = id

    def evaluate(self):
        return identifiers[self.id].value

class ArithmeticExpression(Expression):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def evaluate(self):
        if (self.op == TOKEN_ADD):
            return self.left.evaluate() + self.right.evaluate()

        if (self.op == TOKEN_SUB):
            return self.left.evaluate() - self.right.evaluate()

        if (self.op == TOKEN_MUL):
            return self.left.evaluate() * self.right.evaluate()

        if (self.op == TOKEN_DIV):
            return self.left.evaluate() / self.right.evaluate()

class AssignmentExpression(Expression):
    def __init__(self, id, value):
        self.id = id
        self.value = value

    def evaluate(self):
        identifiers[self.id].value = self.value