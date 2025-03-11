"""Test suite for calculator REPL."""
import pytest
from unittest.mock import patch
from calculator.repl import CalculatorREPL

@pytest.fixture
def repl():
    """Create a REPL instance for testing."""
    return CalculatorREPL()

def test_load_commands(repl):
    """Test command loading."""
    assert 'add' in repl.commands
    assert 'subtract' in repl.commands
    assert 'multiply' in repl.commands
    assert 'divide' in repl.commands

def test_show_menu(repl, capsys):
    """Test menu display."""
    repl.show_menu()
    captured = capsys.readouterr()
    assert "Available commands:" in captured.out
    assert "add:" in captured.out
    assert "subtract:" in captured.out
    assert "multiply:" in captured.out
    assert "divide:" in captured.out
    assert "menu: Show this menu" in captured.out
    assert "exit: Exit the calculator" in captured.out

@pytest.mark.parametrize("input_cmd,args,expected_output", [
    ("add", ["5", "3"], "Result: 8"),
    ("subtract", ["10", "4"], "Result: 6"),
    ("multiply", ["6", "7"], "Result: 42"),
    ("divide", ["15", "3"], "Result: 5"),
])
def test_execute_command_success(repl, input_cmd, args, expected_output, capsys):
    """Test successful command execution."""
    repl.execute_command(input_cmd, args)
    captured = capsys.readouterr()
    assert expected_output in captured.out

@pytest.mark.parametrize("input_cmd,args,expected_output", [
    ("invalid", ["1", "2"], "Unknown command: invalid"),
    ("add", ["1"], "Error: add requires exactly two numbers"),
    ("add", ["1", "2", "3"], "Error: add requires exactly two numbers"),
    ("add", ["abc", "2"], "Error: Invalid number input: abc or 2"),
    ("divide", ["10", "0"], "Error: Cannot divide by zero"),
])
def test_execute_command_errors(repl, input_cmd, args, expected_output, capsys):
    """Test command execution error handling."""
    repl.execute_command(input_cmd, args)
    captured = capsys.readouterr()
    assert expected_output in captured.out

def test_repl_run(repl):
    """Test REPL main loop."""
    with patch('builtins.input') as mock_input:
        mock_input.side_effect = [
            'add 5 3',  # valid command
            'invalid 1 2',  # invalid command
            'menu',  # show menu
            'exit'  # exit loop
        ]
        with patch('builtins.print') as mock_print:
            print(mock_print)
            repl.run()

        # Verify exit was called
        assert mock_input.call_count == 4

def test_repl_keyboard_interrupt(repl):
    """Test REPL keyboard interrupt handling."""
    with patch('builtins.input') as mock_input:
        mock_input.side_effect = [KeyboardInterrupt, 'exit']
        with patch('builtins.print') as mock_print:
            print(mock_print)
            repl.run()
        assert mock_input.call_count == 2

def test_empty_input(repl):
    """Test REPL empty input handling."""
    with patch('builtins.input') as mock_input:
        mock_input.side_effect = ['', 'exit']
        with patch('builtins.print') as mock_print:
            print(mock_print)
            repl.run()
        assert mock_input.call_count == 2
