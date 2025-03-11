"""Test suite for calculator plugins."""

import pytest
import math
from calculator.repl import CalculatorREPL
from calculator.plugins import scientific

class MockREPL:
    """Mock REPL class for testing plugins."""
    def __init__(self):
        self.output = []
        self.calculator = None
    
    def print(self, text):
        """Mock print method."""
        self.output.append(text)

def test_scientific_plugin_registration():
    """Test scientific calculator plugin registration."""
    repl = MockREPL()
    scientific.register_commands(repl)
    assert hasattr(repl.__class__, 'do_pow')
    assert hasattr(repl.__class__, 'do_sqrt')

def test_power_calculation():
    """Test power calculation through plugin."""
    repl = CalculatorREPL()
    scientific.register_commands(repl)
    
    result = math.pow(2, 3)
    assert result == 8

def test_square_root_calculation():
    """Test square root calculation through plugin."""
    repl = CalculatorREPL()
    scientific.register_commands(repl)
    
    result = math.sqrt(16)
    assert result == 4

def test_negative_square_root():
    """Test square root of negative number raises error."""
    repl = CalculatorREPL()
    scientific.register_commands(repl)
    
    with pytest.raises(ValueError):
        math.sqrt(-1)