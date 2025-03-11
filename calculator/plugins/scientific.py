"""Scientific calculator plugin."""

import math
import logging
from typing import Any

logger = logging.getLogger(__name__)

def register_commands(repl: Any) -> None:
    """Register scientific calculator commands with the REPL."""
    
    def do_pow(self, arg: str) -> None:
        """Calculate power: pow X Y (X raised to power Y)"""
        try:
            x, y = map(float, arg.split())
            result = math.pow(x, y)
            print(f"Result: {result}")
            self.calculator.history.add_calculation('pow', x, y, result)
        except ValueError as e:
            print(f"Error: {str(e)}")
            logger.error(f"Error in pow command: {str(e)}")
        except Exception as e:
            print("Invalid input. Format: pow X Y")
            logger.error(f"Invalid input for pow command: {str(e)}")
    
    def do_sqrt(self, arg: str) -> None:
        """Calculate square root: sqrt X"""
        try:
            x = float(arg)
            if x < 0:
                raise ValueError("Cannot calculate square root of negative number")
            result = math.sqrt(x)
            print(f"Result: {result}")
            self.calculator.history.add_calculation('sqrt', x, 0, result)
        except ValueError as e:
            print(f"Error: {str(e)}")
            logger.error(f"Error in sqrt command: {str(e)}")
        except Exception as e:
            print("Invalid input. Format: sqrt X")
            logger.error(f"Invalid input for sqrt command: {str(e)}")
    
    # Add the new commands to the REPL
    setattr(repl.__class__, 'do_pow', do_pow)
    setattr(repl.__class__, 'do_sqrt', do_sqrt)
    logger.info("Scientific calculator plugin registered")