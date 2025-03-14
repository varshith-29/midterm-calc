"""Test suite for calculator REPL functionality."""
import pytest
from unittest.mock import patch, MagicMock
import cmd
import importlib
from calculator.repl import CalculatorREPL
from calculator.main import main

@pytest.fixture
def repl():
    return CalculatorREPL()

def test_repl_initialization(repl):
    assert repl.intro.startswith("Simple Calculator")
    assert repl.prompt == "calc> "
    assert hasattr(repl, "history")
    assert repl.result == 0.0

def test_add_command(repl):
    # Test basic addition
    repl.do_add("5 3")
    assert repl.result == 8.0
    
    # Test invalid input
    repl.do_add("invalid")
    assert repl.result == 8.0  # Result shouldn't change

def test_subtract_command(repl):
    # Test basic subtraction
    repl.do_subtract("10 4")
    assert repl.result == 6.0
    
    # Test invalid input
    repl.do_subtract("invalid")
    assert repl.result == 6.0

def test_multiply_command(repl):
    # Test basic multiplication
    repl.do_multiply("6 7")
    assert repl.result == 42.0
    
    # Test invalid input
    repl.do_multiply("invalid")
    assert repl.result == 42.0

def test_divide_command(repl):
    # Test basic division
    repl.do_divide("15 3")
    assert repl.result == 5.0
    
    # Test division by zero
    repl.do_divide("10 0")
    assert repl.result == 5.0  # Result shouldn't change
    
    # Test invalid input
    repl.do_divide("invalid")
    assert repl.result == 5.0

def test_quit_command(repl):
    assert repl.do_quit("") is True

def test_EOF_command(repl):
    assert repl.do_EOF("") is True

@patch('builtins.print')
def test_history_command(mock_print, repl):
    # Add some calculations
    repl.do_add("5 3")
    repl.do_multiply("2 4")
    
    # Test history display
    repl.do_history("")
    mock_print.assert_called()

@patch('builtins.print')
def test_stats_command(mock_print, repl):
    # Add some calculations
    repl.do_add("5 3")
    repl.do_multiply("2 4")
    
    # Test stats display
    repl.do_stats("")
    mock_print.assert_called()

def test_clear_command(repl):
    # Add some calculations
    repl.do_add("5 3")
    initial_history = repl.history.get_history()
    
    # Clear history
    repl.do_clear("")
    assert len(repl.history.get_history()) == 0
    assert len(initial_history) > 0  # Verify there was history before clearing

@patch('importlib.import_module')
def test_load_plugins(mock_import_module, repl):
    # Mock plugin module
    mock_plugin = MagicMock()
    mock_import_module.return_value = mock_plugin
    
    # Test plugin loading
    repl._load_plugins()
    mock_import_module.assert_called()
    mock_plugin.register_commands.assert_called_with(repl)

@patch('builtins.print')
def test_plugins_command(mock_print, repl):
    repl.do_plugins("")
    mock_print.assert_called()

def test_input_validation():
    repl = CalculatorREPL()
    
    # Test various invalid inputs
    invalid_inputs = [
        "",  # Empty
        "1",  # Missing second number
        "a b",  # Non-numeric
        "1 2 3",  # Too many numbers
        "1.5 invalid",  # Second number invalid
        "invalid 2.0",  # First number invalid
    ]
    
    for invalid_input in invalid_inputs:
        repl.result = 0.0
        repl.do_add(invalid_input)
        assert repl.result == 0.0  # Result should not change
        repl.do_subtract(invalid_input)
        assert repl.result == 0.0
        repl.do_multiply(invalid_input)
        assert repl.result == 0.0
        repl.do_divide(invalid_input)
        assert repl.result == 0.0

@patch('sys.argv', ['calculator'])
@patch('calculator.repl.CalculatorREPL.cmdloop')
def test_main_function(mock_cmdloop):
    """Test the main function of the REPL."""
    # We need to ensure cmdloop doesn't raise KeyboardInterrupt
    mock_cmdloop.return_value = None
    main()
    mock_cmdloop.assert_called_once()

def test_plugin_load_error():
    """Test handling of plugin loading errors."""
    repl = CalculatorREPL()
    
    # Test with non-existent plugin
    with patch.dict('sys.modules', {'calculator.plugins.nonexistent': None}):
        repl._load_plugins()  # Should not raise exception

    # Test with plugin that raises exception
    mock_plugin = MagicMock()
    mock_plugin.register_commands.side_effect = Exception("Plugin error")
    with patch.dict('sys.modules', {'calculator.plugins.mock': mock_plugin}):
        with patch('importlib.import_module', return_value=mock_plugin):
            repl._load_plugins()  # Should not raise exception

@patch('builtins.print')
def test_handle_empty_result(mock_print, repl):
    """Test handling when result is None or invalid."""
    repl.result = None
    repl.do_history("")  # Should handle None result
    mock_print.assert_called()

def test_invalid_plugin_command():
    """Test handling of invalid plugin commands."""
    repl = CalculatorREPL()
    # Call undefined plugin command
    repl.default("invalid_command")  # Should not raise exception

def test_emptyline():
    """Test empty line behavior."""
    repl = CalculatorREPL()
    assert repl.emptyline() is None  # Should not change state

def test_command_help():
    """Test help messages for commands."""
    repl = CalculatorREPL()
    with patch('builtins.print') as mock_print:
        repl.help_add()
        mock_print.assert_called_with("Add the given number to the current result.")
        
        repl.help_subtract()
        mock_print.assert_called_with("Subtract the given number from the current result.")
        
        repl.help_multiply()
        mock_print.assert_called_with("Multiply the current result by the given number.")
        
        repl.help_divide()
        mock_print.assert_called_with("Divide the current result by the given number.")

@patch('calculator.history.CalculationHistory')
def test_history_error_handling(mock_history):
    """Test handling of history-related errors."""
    mock_history_instance = MagicMock()
    mock_history_instance.get_history.side_effect = Exception("History error")
    mock_history_instance.get_statistics.side_effect = Exception("Stats error")
    mock_history.return_value = mock_history_instance
    
    repl = CalculatorREPL()
    
    # These should not raise exceptions
    with patch('builtins.print') as mock_print:
        repl.do_history("")
        mock_print.assert_called()
        
        repl.do_stats("")
        mock_print.assert_called()

@patch('builtins.print')
def test_invalid_command_handling(mock_print, repl):
    """Test handling of various invalid commands."""
    # Test with completely invalid command
    repl.default("invalid")
    mock_print.assert_called()
    
    # Test with invalid parameters
    repl.do_add("not a number")
    assert repl.result == 0.0  # Result should not change

def test_command_completion():
    """Test command name completion."""
    repl = CalculatorREPL()
    
    # Test completion for built-in commands
    assert "add" in repl.completenames("a")
    assert "multiply" in repl.completenames("m")
    assert "divide" in repl.completenames("d")
    assert "quit" in repl.completenames("q")
    
    # Test with non-matching prefix
    assert len(repl.completenames("x")) == 0
    
    # Test with empty prefix
    all_commands = repl.completenames("")
    assert "add" in all_commands
    assert "subtract" in all_commands
    assert "multiply" in all_commands
    assert "divide" in all_commands

def test_repl_lifecycle():
    """Test REPL lifecycle methods."""
    repl = CalculatorREPL()
    
    # Test preloop
    assert repl.preloop() is None
    
    # Test postloop
    assert repl.postloop() is None
    
    # Test precmd
    assert repl.precmd("test") == "test"
    
    # Test postcmd
    assert repl.postcmd(False, "test") is False
    assert repl.postcmd(True, "test") is True

def test_parse_input():
    """Test input parsing functionality."""
    repl = CalculatorREPL()
    
    # Test valid input
    assert repl._parse_input("5 3") == (5.0, 3.0)
    assert repl._parse_input("-2.5 3.7") == (-2.5, 3.7)
    
    # Test invalid inputs
    assert repl._parse_input("") is None
    assert repl._parse_input("abc def") is None
    assert repl._parse_input("1") is None
    assert repl._parse_input("1 2 3") is None
    assert repl._parse_input("1.5 abc") is None

def test_help_system():
    """Test the help system comprehensively."""
    repl = CalculatorREPL()
    with patch('builtins.print') as mock_print:
        # Test individual help messages
        repl.help_add()
        mock_print.assert_called_with("Add the given number to the current result.")
        
        repl.help_subtract()
        mock_print.assert_called_with("Subtract the given number from the current result.")
        
        repl.help_multiply()
        mock_print.assert_called_with("Multiply the current result by the given number.")
        
        repl.help_divide()
        mock_print.assert_called_with("Divide the current result by the given number.")
        
        repl.help_clear()
        mock_print.assert_called_with("Clear the calculation history.")
        
        repl.help_history()
        mock_print.assert_called_with("Show the calculation history.")
        
        repl.help_stats()
        mock_print.assert_called_with("Show statistics about calculations performed.")
        
        repl.help_quit()
        mock_print.assert_called_with("Quit the calculator application.")
        
        repl.help_plugins()
        mock_print.assert_called_with("List available calculator plugins.")

@patch('calculator.history.CalculationHistory.add_calculation')
def test_history_recording(mock_add_calculation, repl):
    """Test that calculations are recorded in history."""
    # Test successful operation recording
    repl.do_add("5 3")
    mock_add_calculation.assert_called_with("+", 5.0, 3.0, 8.0)
    
    repl.do_multiply("4 2")
    mock_add_calculation.assert_called_with("*", 4.0, 2.0, 8.0)
    
    # Test that failed operations are not recorded
    repl.do_add("invalid input")
    assert mock_add_calculation.call_count == 2  # Should not have increased

def test_repl_attributes():
    """Test REPL object attributes."""
    repl = CalculatorREPL()
    
    # Test initial attributes
    assert isinstance(repl.history, CalculationHistory)
    assert repl.result == 0.0
    assert repl.intro.startswith("Simple Calculator")
    assert repl.prompt == "calc> "