"""Tests for the main module."""
import os
import pytest
from unittest.mock import patch, MagicMock
from calculator import __main__
from calculator.config import setup_logging, get_config
from calculator.main import main

def test_run_main():
    """Test the run_main function in __main__ module."""
    result = __main__.run_main()
    assert result == 0

def test_test_main():
    """Test the test_main function in __main__ module."""
    result = __main__.test_main()
    assert result == 0

def test_config_setup_logging():
    """Test setup_logging function."""
    # Test with default values
    with patch('logging.config.dictConfig') as mock_dict_config:
        config = setup_logging()
        mock_dict_config.assert_called_once()
        assert config['loggers']['']['level'] == 'INFO'
        
    # Test with custom environment variables
    with patch.dict(os.environ, {'CALCULATOR_LOG_LEVEL': 'DEBUG'}):
        with patch('logging.config.dictConfig') as mock_dict_config:
            config = setup_logging()
            assert config['loggers']['']['level'] == 'DEBUG'

def test_get_config():
    """Test get_config function."""
    # Test with default value
    assert get_config('NONEXISTENT', 'default') == 'default'
    
    # Test with environment variable
    with patch.dict(os.environ, {'CALCULATOR_TEST': 'value'}):
        assert get_config('TEST') == 'value'

def test_main_normal_exit():
    """Test main function with normal exit."""
    with patch('calculator.repl.CalculatorREPL') as mock_repl_class:
        mock_repl = MagicMock()
        mock_repl_class.return_value = mock_repl
        
        # Normal execution path
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

def test_main_initialization_error():
    """Test main function with initialization error."""
    with patch('calculator.repl.CalculatorREPL', side_effect=Exception("Init error")):
        with patch('calculator.config.setup_logging'):
            with patch('builtins.print') as mock_print:
                with patch('logging.getLogger'):
                    result = main()
                    assert result == 1
                    mock_print.assert_called_with("Failed to initialize calculator: Init error") 