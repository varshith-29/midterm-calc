from calculator.operations import addition, subtraction, multiplication, division
from decimal import Decimal 

class Calculator:
    def __init__(self, history):
        self.history = history

    def add(a, b):
        return addition(a, b)

    def subtract(a: Decimal, b: Decimal) -> Decimal:
        return subtraction(a, b)

    def multiply(a: Decimal, b: Decimal) -> Decimal:
        return multiplication(a, b)

    def divide(a: Decimal, b: Decimal) -> Decimal:
        return division(a, b)