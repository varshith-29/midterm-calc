"""Tests for special cases in scientific plugin."""
import math
import pytest
from calculator.plugins.scientific import ScientificPlugin, register_commands
from tests.test_plugins import MockREPL
from unittest.mock import patch

def test_scientific_special_values():
    """Test scientific operations with special values."""
    repl = MockREPL()
    register_commands(repl)
    
    # Test power with NaN
    repl.result = float('nan')
    repl.do_pow("2")
    assert "nan" in repl.last_printed
    
    # Test power with infinity
    repl.result = float('inf')
    repl.do_pow("2")
    assert "inf" in repl.last_printed
    
    # Test power with infinity and negative exponent
    repl.result = float('inf')
    repl.do_pow("-2")
    assert "0.0" in repl.last_printed
    
    # Test power with infinity and zero exponent
    repl.result = float('inf')
    repl.do_pow("0")
    assert "1.0" in repl.last_printed
    
    # Test sqrt with NaN
    repl.result = float('nan')
    repl.do_sqrt("")
    assert "nan" in repl.last_printed
    
    # Test sqrt with positive infinity
    repl.result = float('inf')
    repl.do_sqrt("")
    assert "inf" in repl.last_printed
    
    # Test sqrt with negative number
    repl.result = -1.0
    repl.do_sqrt("")
    assert "Error" in repl.last_printed
    
    # Test sqrt with argument (should error)
    repl.result = 4.0
    repl.do_sqrt("2")
    assert "Error" in repl.last_printed

def test_scientific_unexpected_errors():
    """Test handling of unexpected errors in scientific operations."""
    repl = MockREPL()
    register_commands(repl)
    
    # Test unexpected error in power calculation
    with patch.object(repl.scientific_plugin, 'power', side_effect=Exception("Unexpected test error")):
        repl.result = 2.0
        repl.do_pow("3")
        assert "Unexpected error" in repl.last_printed
    
    # Test unexpected error in sqrt calculation
    with patch.object(repl.scientific_plugin, 'sqrt', side_effect=Exception("Unexpected test error")):
        repl.result = 4.0
        repl.do_sqrt("")
        assert "Unexpected error" in repl.last_printed 