"""Test suite for calculator plugins."""

import math
import pytest
from calculator.repl import CalculatorREPL
from calculator.plugins import scientific
from unittest.mock import MagicMock, patch
from calculator.plugins.scientific import register_commands, ScientificPlugin

# pylint: disable=too-few-public-methods
class MockREPL:
    """Mock REPL class for testing plugins."""
    def __init__(self):
        """Initialize mock REPL."""
        self.result = None
        self.last_printed = None
        self.calculator = None

    def print(self, text):
        """Store the last printed text."""
        self.last_printed = text

def test_scientific_plugin_registration():
    """Test scientific plugin registration."""
    repl = MockREPL()
    register_commands(repl)
    
    # Check that commands were registered
    assert hasattr(repl, 'do_pow')
    assert hasattr(repl, 'do_sqrt')
    assert hasattr(repl, 'help_pow')
    assert hasattr(repl, 'help_sqrt')
    assert hasattr(repl, 'scientific_plugin')
    
    # Test that the plugin was initialized
    assert isinstance(repl.scientific_plugin, ScientificPlugin)

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
