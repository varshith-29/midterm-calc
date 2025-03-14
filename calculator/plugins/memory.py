"""Memory plugin for calculator."""
import logging
from typing import Optional, Any, Union
from types import MethodType

logger = logging.getLogger(__name__)

def register_commands(repl: Any) -> None:
    """Register memory-related commands with the REPL."""
    if not hasattr(repl, 'memory'):
        repl.memory = None
    
    def do_store(self, arg: str = "") -> None:
        """Store the current result in memory."""
        try:
            if not hasattr(self, 'result'):
                self.print("Error: Result attribute missing")
                return
                
            if self.result is None:
                self.print("Error: Cannot store None value")
                return
                
            try:
                value = float(self.result)
                self.memory = value
                self.print(f"Stored {value} in memory")
            except (ValueError, TypeError):
                self.print("Error: Current result is not a valid number")
        except Exception as e:
            self.print(f"Error: {str(e)}")

    def do_recall(self, arg: str = "") -> None:
        """Recall the value from memory and make it the current result."""
        try:
            if not hasattr(self, 'memory') or self.memory is None:
                self.print("Memory is empty")
                return
                
            try:
                memory_value = float(self.memory)
                self.result = memory_value
                self.print(f"Recalled {memory_value} from memory")
            except (ValueError, TypeError):
                self.print("Error: Memory contains invalid value")
        except Exception as e:
            self.print(f"Error: {str(e)}")

    def do_clear_memory(self, arg: str = "") -> None:
        """Clear the memory."""
        try:
            self.memory = None
            self.print("Memory cleared")
        except Exception as e:
            self.print(f"Error: {str(e)}")

    def do_memory(self, arg: str = "") -> None:
        """Display the current value in memory."""
        try:
            if not hasattr(self, 'memory') or self.memory is None:
                self.print("Memory is empty")
            else:
                if isinstance(self.memory, (int, float)):
                    self.print(f"Memory contains: {self.memory}")
                else:
                    self.print("Error: Memory contains invalid value")
        except Exception as e:
            self.print(f"Error: {str(e)}")

    def help_store(self) -> None:
        """Help for store command."""
        self.print("Store the current result in memory.")

    def help_recall(self) -> None:
        """Help for recall command."""
        self.print("Recall the value from memory and make it the current result.")

    def help_clear_memory(self) -> None:
        """Help for clear_memory command."""
        self.print("Clear the memory.")

    def help_memory(self) -> None:
        """Help for memory command."""
        self.print("Display the current value in memory.")

    # Bind methods to REPL instance
    repl.do_store = MethodType(do_store, repl)
    repl.do_recall = MethodType(do_recall, repl)
    repl.do_clear_memory = MethodType(do_clear_memory, repl)
    repl.do_memory = MethodType(do_memory, repl)
    repl.help_store = MethodType(help_store, repl)
    repl.help_recall = MethodType(help_recall, repl)
    repl.help_clear_memory = MethodType(help_clear_memory, repl)
    repl.help_memory = MethodType(help_memory, repl)
    
    logger.info("Memory plugin registered")