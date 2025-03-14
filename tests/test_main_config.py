"""Tests for main and config functionality."""
import os
import pytest
from unittest.mock import patch, MagicMock
from calculator.config import setup_logging, get_config

def test_config_get_config():
    """Test get_config function."""
    # Test default value
    default_value = "default_test_value"
    result = get_config("NON_EXISTENT_KEY", default_value)
    assert result == default_value
    
    # Test with environment variable
    test_value = "test_config_value"
    with patch.dict(os.environ, {"CALCULATOR_TEST_KEY": test_value}):
        result = get_config("TEST_KEY")
        assert result == test_value

def test_config_setup_logging():
    """Test setup_logging function."""
    # Test with mocked dictConfig to prevent actual logging setup
    with patch('logging.config.dictConfig') as mock_dict_config:
        result = setup_logging()
        
        # Verify dictConfig was called
        mock_dict_config.assert_called_once()
        
        # Verify result structure
        assert isinstance(result, dict)
        assert 'version' in result
        assert 'handlers' in result
        assert 'loggers' in result
        
        # Default log level should be INFO
        assert result['loggers']['']['level'] == 'INFO'
        
    # Test with custom log level
    with patch.dict(os.environ, {"CALCULATOR_LOG_LEVEL": "DEBUG"}):
        with patch('logging.config.dictConfig'):
            result = setup_logging()
            assert result['loggers']['']['level'] == 'DEBUG' 