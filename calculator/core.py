"""Core calculator functionality implementation."""

import logging
from calculator.history import CalculationHistory
from typing import Any, Dict, Optional, Callable

# Set up logging
logger = logging.getLogger(__name__)

class Calculator:
    """Core calculator class implementing basic arithmetic operations."""
    
    def __init__(self):
        """Initialize the calculator with basic operations."""
        self.operations = {
            '+': self.add,
            '-': self.subtract,
            '*': self.multiply,
            '/': self.divide
        }
        self.history = CalculationHistory()
    
    def add(self, x: float, y: float) -> float:
        """Add two numbers."""
        logger.info(f"Adding {x} and {y}")
        return x + y
    
    def subtract(self, x: float, y: float) -> float:
        """Subtract two numbers."""
        logger.info(f"Subtracting {y} from {x}")
        return x - y
    
    def multiply(self, x: float, y: float) -> float:
        """Multiply two numbers."""
        logger.info(f"Multiplying {x} and {y}")
        return x * y
    
    def divide(self, x: float, y: float) -> float:
        """Divide two numbers."""
        if y == 0:
            logger.error("Division by zero attempted")
            raise ValueError("Cannot divide by zero")
        logger.info(f"Dividing {x} by {y}")
        return x / y
    
    def calculate(self, operation: str, x: float, y: float) -> float:
        """Perform the specified calculation."""
        try:
            if operation not in self.operations:
                logger.error(f"Invalid operation attempted: {operation}")
                raise ValueError(f"Unknown operation: {operation}")
            
            result = self.operations[operation](x, y)
            logger.info(f"Calculation result: {result}")
            
            # Add to history
            self.history.add_calculation(operation, x, y, result)
            return result
            
        except Exception as e:
            logger.error(f"Error during calculation: {str(e)}")
            raise
