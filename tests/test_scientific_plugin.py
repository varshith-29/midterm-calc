"""Test suite for scientific calculator plugin."""
import math
import pytest
from unittest.mock import MagicMock, patch
from calculator.plugins.scientific import register_commands, ScientificPlugin
from tests.test_plugins import MockREPL

class MockREPL:
    """Mock REPL for testing scientific plugin."""
    
    def __init__(self):
        """Initialize mock REPL."""
        self.result = None
        self.last_printed = None
        
    def print(self, text):
        """Store the last printed text."""
        self.last_printed = text

def test_scientific_plugin_registration():
    repl = MockREPL()
    register_commands(repl)
    assert hasattr(repl, "do_pow")
    assert hasattr(repl, "do_sqrt")

def test_power_operation():
    repl = MockREPL()
    register_commands(repl)
    
    # Test basic power operation
    repl.result = 2.0
    repl.do_pow("3")
    assert repl.result == 8.0
    
    # Test power with negative exponent
    repl.result = 2.0
    repl.do_pow("-2")
    assert repl.result == 0.25
    
    # Test power with decimal exponent
    repl.result = 4.0
    repl.do_pow("0.5")
    assert repl.result == 2.0

def test_power_invalid_input():
    repl = MockREPL()
    register_commands(repl)
    
    # Test invalid input
    repl.result = 2.0
    repl.do_pow("invalid")
    assert "Error: Invalid input for power operation" in repl.last_printed

def test_sqrt_operation():
    repl = MockREPL()
    register_commands(repl)
    
    # Test basic square root
    repl.result = 16.0
    repl.do_sqrt("")
    assert repl.result == 4.0
    
    # Test square root of zero
    repl.result = 0.0
    repl.do_sqrt("")
    assert repl.result == 0.0

def test_sqrt_negative_number():
    repl = MockREPL()
    register_commands(repl)
    
    # Test square root of negative number
    repl.result = -16.0
    repl.do_sqrt("")
    assert "Error: Cannot calculate square root of negative number" in repl.last_printed

def test_scientific_help_messages():
    """Test help documentation for scientific commands."""
    repl = MockREPL()
    register_commands(repl)
    
    # Power help
    repl.help_pow()
    assert repl.last_printed == "Raise the current result to the given power."
    
    # Square root help
    repl.help_sqrt()
    assert repl.last_printed == "Calculate the square root of the current result."

def test_power_edge_cases():
    """Test edge cases for power operation."""
    repl = MockREPL()
    register_commands(repl)
    
    # Test with zero base
    repl.result = 0.0
    repl.do_pow("2")
    assert repl.result == 0.0
    
    # Test with zero exponent
    repl.result = 5.0
    repl.do_pow("0")
    assert repl.result == 1.0
    
    # Test with infinity
    repl.result = float("inf")
    repl.do_pow("2")
    assert str(repl.result) == "inf"
    
    # Test with NaN
    repl.result = float("nan")
    repl.do_pow("2")
    assert str(repl.result) == "nan"
    
    # Test 1 raised to any power
    repl.result = 1.0
    repl.do_pow("1000000")
    assert repl.result == 1.0

def test_sqrt_edge_cases():
    """Test edge cases for square root operation."""
    repl = MockREPL()
    register_commands(repl)
    
    # Test sqrt of infinity
    repl.result = float("inf")
    repl.do_sqrt("")
    assert str(repl.result) == "inf"
    
    # Test sqrt of NaN
    repl.result = float("nan")
    repl.do_sqrt("")
    assert str(repl.result) == "nan"
    
    # Test sqrt with missing result attribute
    delattr(repl, 'result')
    repl.do_sqrt("")
    assert "Error" in repl.last_printed

def test_scientific_error_handling():
    """Test error handling in scientific operations."""
    repl = MockREPL()
    register_commands(repl)
    
    # Test power with None value
    repl.result = None
    repl.do_pow("2")
    assert "Error" in repl.last_printed
    
    # Test sqrt with None value
    repl.do_sqrt("")
    assert "Error" in repl.last_printed
    
    # Test power with invalid result attribute
    delattr(repl, 'result')
    repl.do_pow("2")
    assert "Error" in repl.last_printed
    
    # Test power with non-numeric result
    repl.result = "not a number"
    repl.do_pow("2")
    assert "Error" in repl.last_printed
    
    # Test sqrt with non-numeric result
    repl.do_sqrt("")
    assert "Error" in repl.last_printed

def test_power_special_cases():
    """Test power operation with special cases."""
    repl = MockREPL()
    register_commands(repl)
    
    # Test negative base with integer power
    repl.result = -2.0
    repl.do_pow("2")
    assert repl.result == 4.0
    
    # Test negative base with fractional power
    repl.result = -2.0
    repl.do_pow("0.5")
    assert "Error" in repl.last_printed
    
    # Test zero with negative power
    repl.result = 0.0
    repl.do_pow("-1")
    assert "Error" in repl.last_printed
    
    # Test very large numbers
    repl.result = 1e200
    repl.do_pow("2")
    assert repl.result == float("inf")

def test_sqrt_special_cases():
    """Test sqrt operation with special cases."""
    repl = MockREPL()
    register_commands(repl)
    
    # Test very small number
    repl.result = 1e-200
    repl.do_sqrt("")
    assert repl.result == 1e-100
    
    # Test very large number
    repl.result = 1e200
    repl.do_sqrt("")
    assert repl.result == 1e100
    
    # Test exact zero
    repl.result = 0.0
    repl.do_sqrt("")
    assert repl.result == 0.0

def test_command_validation():
    """Test command input validation."""
    repl = MockREPL()
    register_commands(repl)
    
    # Test power with missing argument
    repl.result = 2.0
    repl.do_pow("")
    assert "Error" in repl.last_printed
    
    # Test power with multiple arguments
    repl.do_pow("2 3")
    assert "Error" in repl.last_printed
    
    # Test sqrt with unexpected argument
    repl.do_sqrt("2")
    assert "Error" in repl.last_printed

def test_help_system():
    """Test help messages for all commands."""
    repl = MockREPL()
    register_commands(repl)
    
    # Test all help methods
    help_methods = [
        ("help_pow", "Raise the current result to the given power."),
        ("help_sqrt", "Calculate the square root of the current result.")
    ]
    
    for method_name, expected_message in help_methods:
        getattr(repl, method_name)()
        assert repl.last_printed == expected_message

def test_scientific_plugin_methods():
    """Test ScientificPlugin methods directly."""
    plugin = ScientificPlugin()
    
    # Test power method
    assert plugin.power(2.0, 3.0) == 8.0
    assert math.isnan(plugin.power(float('nan'), 2.0))
    assert math.isnan(plugin.power(2.0, float('nan')))
    assert plugin.power(float('inf'), 2.0) == float('inf')
    assert plugin.power(float('inf'), -2.0) == 0.0
    assert plugin.power(float('inf'), 0.0) == 1.0
    
    # Test with very large numbers
    assert plugin.power(1e101, 2.0) == float('inf')
    
    # Test error cases
    with pytest.raises(ValueError):
        plugin.power(-2.0, 0.5)
    with pytest.raises(ValueError):
        plugin.power(0.0, -1.0)
    
    # Test sqrt method
    assert plugin.sqrt(4.0) == 2.0
    assert math.isnan(plugin.sqrt(float('nan')))
    assert plugin.sqrt(float('inf')) == float('inf')
    
    # Test error case
    with pytest.raises(ValueError):
        plugin.sqrt(-1.0)