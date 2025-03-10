"""Arithmetic operation commands."""
from decimal import Decimal
from calculator.commands import Command
from calculator import operations
from calculator.config import logger

class AddCommand(Command):
    """Command to perform addition."""
    
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        logger.info(f"Executing add command with {a} and {b}")
        return operations.addition(a, b)
        
    @classmethod
    def description(cls) -> str:
        return "Add two numbers (Usage: add number1 number2)"

class SubtractCommand(Command):
    """Command to perform subtraction."""
    
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        logger.info(f"Executing subtract command with {a} and {b}")
        return operations.subtraction(a, b)
        
    @classmethod
    def description(cls) -> str:
        return "Subtract two numbers (Usage: subtract number1 number2)"

class MultiplyCommand(Command):
    """Command to perform multiplication."""
    
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        logger.info(f"Executing multiply command with {a} and {b}")
        return operations.multiplication(a, b)
        
    @classmethod
    def description(cls) -> str:
        return "Multiply two numbers (Usage: multiply number1 number2)"

class DivideCommand(Command):
    """Command to perform division."""
    
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        logger.info(f"Executing divide command with {a} and {b}")
        return operations.division(a, b)
        
    @classmethod
    def description(cls) -> str:
        return "Divide two numbers (Usage: divide number1 number2)"