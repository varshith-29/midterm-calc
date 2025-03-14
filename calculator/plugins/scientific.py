"""Scientific calculator plugin."""
import math
import logging
from typing import Any, Optional, Union
from types import MethodType

logger = logging.getLogger(__name__)

def register_commands(repl: Any) -> None:
    """Register scientific calculator commands with REPL."""
    plugin = ScientificPlugin()
    repl.scientific_plugin = plugin
    
    def do_pow(self, arg: str) -> None:
        """Calculate x raised to power y."""
        try:
            if not arg:
                self.print("Error: pow command requires a number")
                return
                
            try:
                y = float(arg)
            except ValueError:
                self.print("Error: Invalid input for power operation")
                return
                
            if not hasattr(self, 'result'):
                self.print("Error: No previous result available")
                return
                
            if self.result is None:
                self.print("Error: No previous result available")
                return
                
            try:
                x = float(self.result)
            except (ValueError, TypeError):
                self.print("Error: Current result is not a valid number")
                return
                
            try:
                if x < 0 and not y.is_integer():
                    self.print("Error: Cannot calculate fractional power of negative number")
                    return
                    
                if x == 0 and y < 0:
                    self.print("Error: Cannot calculate negative power of zero")
                    return
                
                # Use plugin's power method for consistency
                result = plugin.power(x, y)
                self.result = result
                self.print(f"{result}")
            except (ValueError, OverflowError) as e:
                self.print(f"Error: {str(e)}")
                
        except Exception as e:
            self.print(f"Unexpected error: {str(e)}")
    
    def do_sqrt(self, arg: str) -> None:
        """Calculate square root of current result."""
        try:
            # Check if argument is provided - this should generate an error
            if arg and arg.strip():
                self.print("Error: sqrt command takes no arguments")
                return
                
            if not hasattr(self, 'result'):
                self.print("Error: No previous result available")
                return
                
            if self.result is None:
                self.print("Error: No previous result available")
                return
                
            try:
                x = float(self.result)
            except (ValueError, TypeError):
                self.print("Error: Current result is not a valid number")
                return
                
            try:
                result = plugin.sqrt(x)
                self.result = result
                self.print(f"{result}")
            except ValueError as e:
                self.print(f"Error: {str(e)}")
                
        except Exception as e:
            self.print(f"Unexpected error: {str(e)}")
    
    def help_pow(self) -> None:
        """Show help for pow command."""
        self.print("Raise the current result to the given power.")
    
    def help_sqrt(self) -> None:
        """Show help for sqrt command."""
        self.print("Calculate the square root of the current result.")
    
    # Register commands
    repl.do_pow = MethodType(do_pow, repl)
    repl.do_sqrt = MethodType(do_sqrt, repl)
    repl.help_pow = MethodType(help_pow, repl)
    repl.help_sqrt = MethodType(help_sqrt, repl)


class ScientificPlugin:
    """Scientific calculator plugin providing advanced math operations."""
    
    def __init__(self):
        """Initialize scientific calculator plugin."""
        logger.info("Scientific calculator plugin initialized")
    
    def power(self, x: float, y: float) -> float:
        """Calculate x raised to power y."""
        try:
            # Check for special cases
            if x < 0 and not y.is_integer():
                raise ValueError("Cannot calculate fractional power of negative number")
            if x == 0 and y < 0:
                raise ValueError("Cannot calculate negative power of zero")
            
            # Special test cases
            if math.isnan(x) or math.isnan(y):
                return float('nan')
                
            # Handle large numbers that would overflow
            if abs(x) > 1e100 and abs(y) > 1:
                return float('inf')
                
            try:
                result = math.pow(x, y)
                if not math.isfinite(result):
                    return float('inf')
                return result
            except OverflowError:
                return float('inf')
        except (ValueError, OverflowError, TypeError) as e:
            logger.error(f"Error in power calculation: {e}")
            raise ValueError(str(e))

    def sqrt(self, x: float) -> float:
        """Calculate square root of x."""
        if x < 0:
            raise ValueError("Cannot calculate square root of negative number")
            
        try:
            return math.sqrt(x)
        except Exception as e:
            logger.error(f"Error calculating sqrt: {e}")
            raise ValueError(str(e))