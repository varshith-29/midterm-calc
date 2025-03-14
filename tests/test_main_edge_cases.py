"""Tests for edge cases in main module."""
import pytest
from unittest.mock import patch, MagicMock
from calculator.main import main

def test_main_normal_exit():
    """Test main function with normal exit."""
    with patch('calculator.repl.CalculatorREPL') as mock_repl_class:
        mock_repl = MagicMock()
        mock_repl_class.return_value = mock_repl
        
        with patch('calculator.config.setup_logging'):
            with patch('logging.getLogger'):
                result = main()
                assert result == 0
                mock_repl.cmdloop.assert_called_once()

def test_main_keyboard_interrupt():
    """Test main function with keyboard interrupt."""
    with patch('calculator.repl.CalculatorREPL') as mock_repl_class:
        mock_repl = MagicMock()
        mock_repl_class.return_value = mock_repl
        mock_repl.cmdloop.side_effect = KeyboardInterrupt()
        
        with patch('calculator.config.setup_logging'):
            with patch('builtins.print') as mock_print:
                with patch('logging.getLogger'):
                    result = main()
                    assert result == 0
                    mock_print.assert_called_with("\nGoodbye!")

def test_main_unexpected_error():
    """Test main function with unexpected error."""
    with patch('calculator.repl.CalculatorREPL') as mock_repl_class:
        mock_repl = MagicMock()
        mock_repl_class.return_value = mock_repl
        mock_repl.cmdloop.side_effect = Exception("Test error")
        
        with patch('calculator.config.setup_logging'):
            with patch('builtins.print') as mock_print:
                with patch('logging.getLogger'):
                    result = main()
                    assert result == 1
                    mock_print.assert_called_with("An unexpected error occurred: Test error") 