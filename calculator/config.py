"""Configuration settings for the calculator application."""

import os
import logging.config
from typing import Dict

def setup_logging() -> None:
    """Configure logging based on environment variables."""
    log_level = os.getenv('CALCULATOR_LOG_LEVEL', 'INFO').upper()
    log_file = os.getenv('CALCULATOR_LOG_FILE', 'calculator.log')
    
    logging_config: Dict = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': log_level,
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
            },
            'file': {
                'level': log_level,
                'formatter': 'standard',
                'class': 'logging.FileHandler',
                'filename': log_file,
                'mode': 'a',
            }
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['console', 'file'],
                'level': log_level,
                'propagate': True
            }
        }
    }
    
    logging.config.dictConfig(logging_config)
    logging.info(f"Logging configured with level {log_level}")