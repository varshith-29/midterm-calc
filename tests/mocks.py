"""Mock classes for testing calculator plugins."""
from typing import List, Optional, Any

class MockREPL:
    """Mock REPL class for testing plugins."""
    
    def __init__(self):
        """Initialize mock REPL."""
        self.result = 0.0
        self.memory = None
        self.last_printed = None
        self.output = []
    
    def print(self, text):
        """Mock print method to capture output."""
        self.last_printed = text
        self.output.append(text) 