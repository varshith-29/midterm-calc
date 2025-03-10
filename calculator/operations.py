from decimal import Decimal
from calculator.config import logger

def addition(a: Decimal, b: Decimal) -> Decimal:
    logger.debug(f"Adding {a} + {b}")
    return a + b

def subtraction(a: Decimal, b: Decimal) -> Decimal:
    logger.debug(f"Subtracting {a} - {b}")
    return a - b

def multiplication(a: Decimal, b: Decimal) -> Decimal:
    logger.debug(f"Multiplying {a} * {b}")
    return a * b

def division(a: Decimal, b: Decimal) -> Decimal:
    logger.debug(f"Dividing {a} / {b}")
    if b == 0:
        logger.error("Division by zero attempted")
        raise ValueError("Cannot divide by zero")
    return a / b