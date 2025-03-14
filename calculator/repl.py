"""REPL interface for the calculator application."""
import cmd
import logging
import shlex
import os
import importlib
from typing import List, Optional, Any, Dict, Tuple

from calculator.core import Calculator
from calculator.history import CalculationHistory

__all__ = ['CalculatorREPL']

logger = logging.getLogger(__name__)

class CalculatorREPL(cmd.Cmd):
    """Interactive calculator REPL interface."""
    prompt = 'calc> '
    intro = 'Simple Calculator. Type help or ? for command list.'

    def __init__(self):
        """Initialize the calculator REPL."""
        super().__init__()
        self.calculator = Calculator()
        self.history = self.calculator.history
        self.result = 0.0
        self._load_plugins()

    def _parse_input(self, arg: str) -> Optional[Tuple[float, float]]:
        """Parse space-separated numbers from input string."""
        try:
            numbers = shlex.split(arg)
            if len(numbers) != 2:
                self.print("Error: Please provide exactly two numbers")
                return None
            return (float(numbers[0]), float(numbers[1]))
        except ValueError:
            self.print("Error: Please provide valid numbers")
            return None

    def do_add(self, arg: str) -> None:
        """Add two numbers."""
        numbers = self._parse_input(arg)
        if numbers:
            x, y = numbers
            try:
                self.result = self.calculator.calculate('+', x, y)
                self.print(f"{self.result}")
            except Exception as e:
                self.print(f"Error: {str(e)}")

    def help_add(self) -> None:
        """Show help for add command."""
        self.print("Add the given number to the current result.")

    def do_subtract(self, arg: str) -> None:
        """Subtract numbers."""
        numbers = self._parse_input(arg)
        if numbers:
            x, y = numbers
            try:
                self.result = self.calculator.calculate('-', x, y)
                self.print(f"{self.result}")
            except Exception as e:
                self.print(f"Error: {str(e)}")

    def help_subtract(self) -> None:
        """Show help for subtract command."""
        self.print("Subtract the given number from the current result.")

    def do_multiply(self, arg: str) -> None:
        """Multiply numbers."""
        numbers = self._parse_input(arg)
        if numbers:
            x, y = numbers
            try:
                self.result = self.calculator.calculate('*', x, y)
                self.print(f"{self.result}")
            except Exception as e:
                self.print(f"Error: {str(e)}")

    def help_multiply(self) -> None:
        """Show help for multiply command."""
        self.print("Multiply the current result by the given number.")

    def do_divide(self, arg: str) -> None:
        """Divide numbers."""
        numbers = self._parse_input(arg)
        if numbers:
            x, y = numbers
            try:
                self.result = self.calculator.calculate('/', x, y)
                self.print(f"{self.result}")
            except Exception as e:
                self.print(f"Error: {str(e)}")

    def help_divide(self) -> None:
        """Show help for divide command."""
        self.print("Divide the current result by the given number.")

    def do_history(self, arg: str) -> None:
        """Show calculation history."""
        try:
            limit = None
            if arg:
                try:
                    limit = int(arg)
                    if limit <= 0:
                        self.print("Error: Limit must be a positive integer")
                        return
                except ValueError:
                    self.print("Error: Limit must be a positive integer")
                    return
            
            df = self.history.get_history(limit)
            if df.empty:
                self.print("No calculation history")
            else:
                # Format for display
                formatted = df.copy()
                formatted['timestamp'] = formatted['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
                self.print(formatted.to_string(index=False))
        except Exception as e:
            self.print(f"Error: {str(e)}")

    def help_history(self) -> None:
        """Show help for history command."""
        self.print("Show the calculation history.")

    def do_stats(self, arg: str) -> None:
        """Show calculation statistics."""
        try:
            stats = self.history.get_statistics()
            self.print("Calculation Statistics:")
            self.print(f"Total calculations: {stats['total_calculations']}")
            
            if stats['total_calculations'] > 0:
                self.print("Operations:")
                for op, count in stats['operations_count'].items():
                    self.print(f"  {op}: {count}")
                
                self.print(f"Average result: {stats['average_result']:.4f}")
                self.print(f"Max result: {stats['max_result']}")
                self.print(f"Min result: {stats['min_result']}")
        except Exception as e:
            self.print(f"Error: {str(e)}")

    def help_stats(self) -> None:
        """Show help for stats command."""
        self.print("Show statistics about calculations performed.")

    def do_clear(self, arg: str) -> None:
        """Clear calculation history."""
        try:
            self.history.clear_history()
            self.print("Calculation history cleared")
        except Exception as e:
            self.print(f"Error: {str(e)}")

    def help_clear(self) -> None:
        """Show help for clear command."""
        self.print("Clear the calculation history.")

    def do_quit(self, arg: str) -> bool:
        """Quit the calculator."""
        self.print("\nGoodbye!")
        return True

    def help_quit(self) -> None:
        """Show help for quit command."""
        self.print("Quit the calculator application.")

    def do_EOF(self, arg: str) -> bool:
        """Handle EOF (Ctrl+D)."""
        return self.do_quit(arg)

    def _load_plugins(self) -> None:
        """Load calculator plugins."""
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
        plugin_dir = os.path.join(plugin_dir, 'plugins')
        
        if not os.path.exists(plugin_dir):
            logger.warning(f"Plugin directory not found: {plugin_dir}")
            return

        for filename in os.listdir(plugin_dir):
            if filename.endswith('.py') and not filename.startswith('__'):
                try:
                    module_name = f"calculator.plugins.{filename[:-3]}"
                    module = importlib.import_module(module_name)
                    if hasattr(module, 'register_commands'):
                        module.register_commands(self)
                        logger.info(f"Plugin registered: {filename}")
                    else:
                        logger.warning(f"No register_commands function in {module_name}")
                except Exception as e:
                    logger.error(f"Error loading plugin {filename}: {str(e)}")

    def do_plugins(self, arg: str) -> None:
        """List available plugins."""
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
        plugin_dir = os.path.join(plugin_dir, 'plugins')
        
        try:
            plugins = [f[:-3] for f in os.listdir(plugin_dir)
                   if f.endswith('.py') and not f.startswith('__')]
            self.print(f"Available plugins: {', '.join(plugins)}")
        except Exception as e:
            self.print(f"Error listing plugins: {str(e)}")

    def help_plugins(self) -> None:
        """Show help for plugins command."""
        self.print("List available calculator plugins.")

    def print(self, text: str) -> None:
        """Print text to output."""
        print(text)
        
    def default(self, line: str) -> None:
        """Handle unknown commands."""
        self.print(f"Unknown command: {line}")
        
    def emptyline(self) -> None:
        """Handle empty lines."""
        pass