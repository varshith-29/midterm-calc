"""Memory operations plugin."""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

def register_commands(repl: Any) -> None:
    """Register memory operation commands with the REPL."""
    
    # Add memory storage to the REPL instance
    if not hasattr(repl, 'memory'):
        repl.memory: Dict[str, float] = {}
    
    def do_store(self, arg: str) -> None:
        """Store a value in memory: store NAME VALUE"""
        try:
            name, value = arg.split()
            value = float(value)
            self.memory[name] = value
            print(f"Stored {value} in {name}")
            logger.info(f"Stored value {value} in memory location {name}")
        except ValueError:
            print("Invalid input. Format: store NAME VALUE")
            logger.error("Invalid store command format")
    
    def do_recall(self, arg: str) -> None:
        """Recall a value from memory: recall NAME"""
        try:
            name = arg.strip()
            if name in self.memory:
                value = self.memory[name]
                print(f"{name}: {value}")
                logger.info(f"Recalled value {value} from memory location {name}")
            else:
                print(f"No value stored in {name}")
                logger.warning(f"Attempted to recall non-existent memory location {name}")
        except Exception as e:
            print(f"Error recalling value: {str(e)}")
            logger.error(f"Error in recall command: {str(e)}")
    
    def do_clear_memory(self, arg: str) -> None:
        """Clear all stored memory values"""
        self.memory.clear()
        print("Memory cleared")
        logger.info("Memory cleared")
    
    def do_memory(self, arg: str) -> None:
        """List all stored memory values"""
        if not self.memory:
            print("No values in memory")
            return
        print("\nStored Memory Values:")
        for name, value in self.memory.items():
            print(f"  {name}: {value}")
    
    # Add the new commands to the REPL
    setattr(repl.__class__, 'do_store', do_store)
    setattr(repl.__class__, 'do_recall', do_recall)
    setattr(repl.__class__, 'do_clear_memory', do_clear_memory)
    setattr(repl.__class__, 'do_memory', do_memory)
    logger.info("Memory operations plugin registered")