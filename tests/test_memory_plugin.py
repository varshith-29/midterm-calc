"""Test suite for memory plugin operations."""
import pytest
from calculator.plugins.memory import register_commands

class MockREPL:
    def __init__(self):
        self.memory = None
        self.last_printed = None
        self.result = 0.0
    
    def print(self, text):
        self.last_printed = text

def test_memory_plugin_registration():
    repl = MockREPL()
    register_commands(repl)
    assert hasattr(repl, "do_store")
    assert hasattr(repl, "do_recall")
    assert hasattr(repl, "do_clear_memory")
    assert hasattr(repl, "do_memory")

def test_store_operation():
    repl = MockREPL()
    register_commands(repl)
    
    # Test storing a value
    repl.result = 42.0
    repl.do_store("")
    assert repl.memory == 42.0
    assert repl.last_printed == "Stored 42.0 in memory"

def test_recall_operation():
    repl = MockREPL()
    register_commands(repl)
    
    # Test recalling when memory is empty
    repl.do_recall("")
    assert repl.last_printed == "Memory is empty"
    
    # Test storing and recalling a value
    repl.result = 42.0
    repl.do_store("")
    repl.result = 0.0  # Reset result
    repl.do_recall("")
    assert repl.result == 42.0
    assert repl.last_printed == "Recalled 42.0 from memory"

def test_clear_memory_operation():
    repl = MockREPL()
    register_commands(repl)
    
    # Store a value and then clear it
    repl.result = 42.0
    repl.do_store("")
    repl.do_clear_memory("")
    assert repl.memory is None
    assert repl.last_printed == "Memory cleared"

def test_memory_status():
    repl = MockREPL()
    register_commands(repl)
    
    # Test empty memory status
    repl.do_memory("")
    assert repl.last_printed == "Memory is empty"
    
    # Test memory status with stored value
    repl.result = 42.0
    repl.do_store("")
    repl.do_memory("")
    assert repl.last_printed == "Memory contains: 42.0"

def test_memory_help_messages():
    """Test help documentation for memory commands."""
    repl = MockREPL()
    register_commands(repl)
    
    # Store help
    repl.help_store()
    assert repl.last_printed == "Store the current result in memory."
    
    # Recall help
    repl.help_recall()
    assert repl.last_printed == "Recall the value from memory and make it the current result."
    
    # Clear help
    repl.help_clear_memory()
    assert repl.last_printed == "Clear the memory."
    
    # Memory status help
    repl.help_memory()
    assert repl.last_printed == "Display the current value in memory."

def test_memory_edge_cases():
    """Test edge cases for memory operations."""
    repl = MockREPL()
    register_commands(repl)
    
    # Store and recall None value
    repl.result = None
    repl.do_store("")
    assert repl.last_printed == "Error: Cannot store None value"
    
    # Store and recall infinity
    repl.result = float("inf")
    repl.do_store("")
    repl.result = 0.0
    repl.do_recall("")
    assert repl.result == float("inf")
    
    # Store and recall NaN
    repl.result = float("nan")
    repl.do_store("")
    repl.result = 0.0
    repl.do_recall("")
    assert str(repl.result) == "nan"
    
    # Clear memory multiple times
    repl.do_clear_memory("")
    repl.do_clear_memory("")  # Second clear shouldn't cause issues
    assert repl.memory is None

def test_memory_error_handling():
    """Test error handling in memory operations."""
    repl = MockREPL()
    register_commands(repl)
    
    # Test recall with no prior store
    repl.do_recall("")
    assert repl.last_printed == "Memory is empty"
    assert repl.result == 0.0
    
    # Test memory status with corrupted memory state
    repl.memory = "invalid"
    repl.do_memory("")
    assert "Error" in repl.last_printed

    # Test store with invalid result attribute
    delattr(repl, 'result')
    repl.do_store("")
    assert "Error" in repl.last_printed
    
    # Test store when result is not a number
    repl.result = "not a number"
    repl.do_store("")
    assert "Error" in repl.last_printed
    
    # Test recall when memory value is invalid
    repl.memory = "not a number"
    repl.do_recall("")
    assert "Error" in repl.last_printed

def test_memory_command_registration():
    """Test registration of memory commands in detail."""
    repl = MockREPL()
    
    # Before registration
    assert not hasattr(repl, "do_store")
    assert not hasattr(repl, "do_recall")
    assert not hasattr(repl, "do_clear_memory")
    assert not hasattr(repl, "do_memory")
    assert not hasattr(repl, "help_store")
    assert not hasattr(repl, "help_recall")
    assert not hasattr(repl, "help_clear_memory")
    assert not hasattr(repl, "help_memory")
    
    # Register commands
    register_commands(repl)
    
    # After registration
    assert hasattr(repl, "do_store")
    assert hasattr(repl, "do_recall")
    assert hasattr(repl, "do_clear_memory")
    assert hasattr(repl, "do_memory")
    assert hasattr(repl, "help_store")
    assert hasattr(repl, "help_recall")
    assert hasattr(repl, "help_clear_memory")
    assert hasattr(repl, "help_memory")

def test_memory_state_transitions():
    """Test memory state transitions through different operations."""
    repl = MockREPL()
    register_commands(repl)
    
    # Initial state
    assert repl.memory is None
    repl.do_memory("")
    assert repl.last_printed == "Memory is empty"
    
    # Store value
    repl.result = 42.0
    repl.do_store("")
    assert repl.memory == 42.0
    
    # Update stored value
    repl.result = 123.0
    repl.do_store("")
    assert repl.memory == 123.0
    
    # Recall value
    repl.result = 0.0
    repl.do_recall("")
    assert repl.result == 123.0
    
    # Clear memory
    repl.do_clear_memory("")
    assert repl.memory is None
    
    # Store after clear
    repl.result = 42.0
    repl.do_store("")
    assert repl.memory == 42.0

def test_memory_special_cases():
    """Test memory operations with special numeric cases."""
    repl = MockREPL()
    register_commands(repl)
    
    # Test with zero
    repl.result = 0.0
    repl.do_store("")
    assert repl.memory == 0.0
    
    # Test with very large number
    repl.result = 1e308
    repl.do_store("")
    assert repl.memory == 1e308
    
    # Test with very small number
    repl.result = 1e-308
    repl.do_store("")
    assert repl.memory == 1e-308