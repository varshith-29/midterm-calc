"""Configuration settings for the calculator application."""

import os
import logging
import logging.config
from typing import Dict, Any, Optional

def setup_logging() -> Dict[str, Any]:
    """Configure logging based on environment variables.
    
    Returns:
        Dictionary with the logging configuration that was applied
    """
    log_level = os.getenv('CALCULATOR_LOG_LEVEL', 'INFO').upper()
    log_file = os.getenv('CALCULATOR_LOG_FILE', 'calculator.log')
    
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': log_level,
                'formatter': 'standard',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.FileHandler',
                'level': log_level,
                'formatter': 'standard',
                'filename': log_file,
                'mode': 'a',
            }
        },
        'loggers': {
            '': {
                'handlers': ['console', 'file'],
                'level': log_level,
                'propagate': True
            }
        }
    }
    
    logging.config.dictConfig(logging_config)
    logging.info(f"Logging configured with level {log_level}")
    return logging_config


def get_config(name: str, default: Any = None) -> Any:
    """Get configuration value from environment variable.
    
    Args:
        name: Name of configuration variable
        default: Default value if not set
        
    Returns:
        Configuration value
    """
    env_var = f"CALCULATOR_{name.upper()}"
    return os.getenv(env_var, default)