"""REPL implementation for calculator."""
import importlib
import inspect
import pkgutil
from decimal import Decimal, InvalidOperation
from typing import Dict, Type
from calculator.commands import Command
import calculator.commands
from calculator.config import logger, get_config

class CalculatorREPL:
    """Interactive calculator REPL implementation."""
    
    def __init__(self):
        self.commands: Dict[str, Type[Command]] = {}
        self.config = get_config()
        logger.debug(f"Initializing Calculator REPL with config: {self.config}")
        self.load_commands()
    
    def load_commands(self):
        """Automatically load all command plugins."""
        # Clear existing commands
        self.commands.clear()
        logger.info("Loading calculator commands")
        
        # Load all modules in the commands package
        for _, name, _ in pkgutil.iter_modules(calculator.commands.__path__):
            module = importlib.import_module(f'calculator.commands.{name}')
            
            # Find all Command subclasses in the module
            for item_name, item in inspect.getmembers(module):
                if (inspect.isclass(item) and 
                    issubclass(item, Command) and 
                    item != Command):
                    command_name = item_name.replace('Command', '').lower()
                    self.commands[command_name] = item
    
    def show_menu(self):
        """Display available commands."""
        print("\nAvailable commands:")
        print("------------------")
        for name, command in sorted(self.commands.items()):
            print(f"{name}: {command.description()}")
        print("\nmenu: Show this menu")
        print("exit: Exit the calculator")
        print()
    
    def execute_command(self, command_name: str, args: list[str]) -> bool:
        """Execute a command with given arguments."""
        if command_name not in self.commands:
            print(f"Unknown command: {command_name}")
            return True
            
        if len(args) != 2:
            print(f"Error: {command_name} requires exactly two numbers")
            return True
            
        try:
            a = Decimal(args[0])
            b = Decimal(args[1])
        except InvalidOperation:
            print(f"Error: Invalid number input: {args[0]} or {args[1]}")
            return True
            
        try:
            command = self.commands[command_name]()
            result = command.execute(a, b)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
            
        return True
    
    def run(self):
        """Start the REPL loop."""
        logger.info("Starting calculator REPL")
        print("Welcome to the Calculator!")
        self.show_menu()
        
        while True:
            try:
                user_input = input("calc> ").strip().lower()
                if not user_input:
                    continue
                    
                parts = user_input.split()
                command = parts[0]
                args = parts[1:]
                logger.debug(f"Executing command: {command} with args: {args}")
                
                if command == 'exit':
                    break
                elif command == 'menu':
                    self.show_menu()
                else:
                    self.execute_command(command, args)
                    
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
            except Exception as e:
                print(f"An error occurred: {e}")
                
        print("Goodbye!")