"""Combined tests for main and config modules."""
import os
import pytest
from unittest.mock import patch, MagicMock
from calculator.main import main
from calculator.config import setup_logging, get_config

def test_get_config():
    """Test get_config function."""
    # Test with default value
    assert get_config('NONEXISTENT', 'default') == 'default'
    
    # Test with environment variable
    with patch.dict(os.environ, {'CALCULATOR_TEST': 'value'}):
        assert get_config('TEST') == 'value'

def test_setup_logging():
    """Test setup_logging function."""
    with patch('logging.config.dictConfig') as mock_dict_config:
        config = setup_logging()
        mock_dict_config.assert_called_once()
        assert 'version' in config
        assert 'handlers' in config
        assert 'loggers' in config

def test_main_successful_execution():
    """Test main function with successful execution."""
    with patch('calculator.repl.CalculatorREPL') as mock_repl_class:
        mock_repl = MagicMock()
        mock_repl_class.return_value = mock_repl
        
        with patch('calculator.config.setup_logging'):
            with patch('logging.getLogger'):
                result = main()
                assert result == 0
                mock_repl.cmdloop.assert_called_once() 