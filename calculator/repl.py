"""REPL interface for the calculator application."""

import cmd
import logging
import importlib
import pkgutil
from typing import Optional, Dict, Any
from .core import Calculator
from .config import setup_logging

logger = logging.getLogger(__name__)

class CalculatorREPL(cmd.Cmd):
    """Command-line interface for the calculator."""
    
    intro = 'Welcome to the Calculator! Type help or ? to list commands.\n'
    prompt = 'calc> '
    
    def __init__(self):
        """Initialize the REPL interface."""
        super().__init__()
        setup_logging()  # Initialize logging configuration
        self.calculator = Calculator()
        self.plugins: Dict[str, Any] = {}
        self._load_plugins()
        logger.info("Calculator REPL initialized")
    
    def do_add(self, arg: str) -> None:
        """Add two numbers: add X Y"""
        try:
            x, y = map(float, arg.split())
            result = self.calculator.calculate('+', x, y)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {str(e)}")
            logger.error(f"Error in add command: {str(e)}")
        except Exception as e:
            print("Invalid input. Format: add X Y")
            logger.error(f"Invalid input for add command: {str(e)}")
    
    def do_subtract(self, arg: str) -> None:
        """Subtract two numbers: subtract X Y"""
        try:
            x, y = map(float, arg.split())
            result = self.calculator.calculate('-', x, y)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {str(e)}")
            logger.error(f"Error in subtract command: {str(e)}")
        except Exception as e:
            print("Invalid input. Format: subtract X Y")
            logger.error(f"Invalid input for subtract command: {str(e)}")
    
    def do_multiply(self, arg: str) -> None:
        """Multiply two numbers: multiply X Y"""
        try:
            x, y = map(float, arg.split())
            result = self.calculator.calculate('*', x, y)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {str(e)}")
            logger.error(f"Error in multiply command: {str(e)}")
        except Exception as e:
            print("Invalid input. Format: multiply X Y")
            logger.error(f"Invalid input for multiply command: {str(e)}")
    
    def do_divide(self, arg: str) -> None:
        """Divide two numbers: divide X Y"""
        try:
            x, y = map(float, arg.split())
            result = self.calculator.calculate('/', x, y)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {str(e)}")
            logger.error(f"Error in divide command: {str(e)}")
        except Exception as e:
            print("Invalid input. Format: divide X Y")
            logger.error(f"Invalid input for divide command: {str(e)}")
    
    def do_quit(self, arg: str) -> bool:
        """Exit the calculator"""
        logger.info("Exiting calculator")
        print("Goodbye!")
        return True
    
    def do_EOF(self, arg: str) -> bool:
        """Handle EOF (Ctrl+D)"""
        return self.do_quit(arg)
    
    def do_history(self, arg: str) -> None:
        """Show calculation history: history [limit]"""
        try:
            limit = int(arg) if arg else None
            history = self.calculator.history.get_history(limit)
            if history.empty:
                print("No calculations in history.")
                return
            print("\nCalculation History:")
            print(history.to_string(index=False))
        except ValueError:
            print("Invalid limit value. Please provide a number.")
            logger.error("Invalid history limit provided")
        except Exception as e:
            print(f"Error retrieving history: {str(e)}")
            logger.error(f"Error in history command: {str(e)}")
    
    def do_stats(self, arg: str) -> None:
        """Show calculation statistics"""
        try:
            stats = self.calculator.history.get_statistics()
            print("\nCalculation Statistics:")
            print(f"Total calculations: {stats['total_calculations']}")
            print("\nOperations breakdown:")
            for op, count in stats['operations_count'].items():
                print(f"  {op}: {count}")
            print(f"\nAverage result: {stats['average_result']:.2f}")
            print(f"Maximum result: {stats['max_result']}")
            print(f"Minimum result: {stats['min_result']}")
        except Exception as e:
            print(f"Error retrieving statistics: {str(e)}")
            logger.error(f"Error in stats command: {str(e)}")
    
    def do_clear(self, arg: str) -> None:
        """Clear calculation history"""
        try:
            self.calculator.history.clear_history()
            print("History cleared successfully.")
        except Exception as e:
            print(f"Error clearing history: {str(e)}")
            logger.error(f"Error in clear command: {str(e)}")
    
    def _load_plugins(self) -> None:
        """Load calculator plugins from the plugins directory."""
        try:
            import calculator.plugins
            for _, name, _ in pkgutil.iter_modules(calculator.plugins.__path__):
                try:
                    plugin = importlib.import_module(f"calculator.plugins.{name}")
                    if hasattr(plugin, 'register_commands'):
                        plugin.register_commands(self)
                        self.plugins[name] = plugin
                        logger.info(f"Loaded plugin: {name}")
                except Exception as e:
                    logger.error(f"Error loading plugin {name}: {str(e)}")
        except Exception as e:
            logger.error(f"Error loading plugins: {str(e)}")
    
    def do_plugins(self, arg: str) -> None:
        """List all available plugins"""
        if not self.plugins:
            print("No plugins loaded.")
            return
        print("\nAvailable Plugins:")
        for name in self.plugins:
            print(f"  - {name}")

def main():
    """Main entry point for the calculator REPL."""
    try:
        CalculatorREPL().cmdloop()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        logger.info("Calculator terminated by keyboard interrupt")
    except Exception as e:
        logger.error(f"Unexpected error in calculator REPL: {str(e)}")
        raise

if __name__ == '__main__':
    main()