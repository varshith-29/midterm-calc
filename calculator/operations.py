from decimal import Decimal

def addition(a: Decimal, b: Decimal) -> Decimal:
    return a + b

def subtraction(a: Decimal, b: Decimal) -> Decimal:
    return a - b

def multiplication(a: Decimal, b: Decimal) -> Decimal:
    return a * b

def division(a: Decimal, b: Decimal) -> Decimal:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b