"""Configuration and environment variables for the calculator application."""
import os
import logging
from pathlib import Path

# Set up logging
LOG_LEVEL = os.environ.get('CALCULATOR_LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Environment variables
ENV = os.environ.get('CALCULATOR_ENV', 'development')

# Create logs directory if it doesn't exist
logs_dir = Path('logs')
logs_dir.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(logs_dir / 'calculator.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('calculator')
logger.info(f"Starting calculator in {ENV} environment")

# Application configuration based on environment
def get_config():
    """Return configuration based on environment."""
    config = {
        'env': ENV,
        'debug': ENV == 'development',
    }
    logger.debug(f"Loaded configuration: {config}")
    return config