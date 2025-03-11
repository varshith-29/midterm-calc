"""History management for calculator operations using pandas."""

import os
import logging
import pandas as pd
from datetime import datetime
from typing import Optional, List, Dict

logger = logging.getLogger(__name__)

class CalculationHistory:
    """Manages calculation history using pandas DataFrame."""
    
    def __init__(self, history_file: str = "calculator_history.csv"):
        """Initialize the history manager."""
        self.history_file = history_file
        self.history: pd.DataFrame = self._load_history()
        logger.info("Calculation history manager initialized")
    
    def _load_history(self) -> pd.DataFrame:
        """Load history from CSV file or create new DataFrame."""
        try:
            if os.path.exists(self.history_file):
                df = pd.read_csv(self.history_file)
                logger.info(f"Loaded history from {self.history_file}")
                return df
        except Exception as e:
            logger.error(f"Error loading history file: {str(e)}")
        
        # Create new DataFrame if file doesn't exist or there's an error
        return pd.DataFrame(columns=['timestamp', 'operation', 'x', 'y', 'result'])
    
    def add_calculation(self, operation: str, x: float, y: float, result: float) -> None:
        """Add a new calculation to history."""
        try:
            new_record = {
                'timestamp': datetime.now(),
                'operation': operation,
                'x': x,
                'y': y,
                'result': result
            }
            self.history = pd.concat([self.history, pd.DataFrame([new_record])], 
                                   ignore_index=True)
            self._save_history()
            logger.info(f"Added calculation to history: {operation} {x} {y} = {result}")
        except Exception as e:
            logger.error(f"Error adding calculation to history: {str(e)}")
            raise
    
    def _save_history(self) -> None:
        """Save history to CSV file."""
        try:
            self.history.to_csv(self.history_file, index=False)
            logger.info(f"Saved history to {self.history_file}")
        except Exception as e:
            logger.error(f"Error saving history: {str(e)}")
            raise
    
    def get_history(self, limit: Optional[int] = None) -> pd.DataFrame:
        """Retrieve calculation history, optionally limited to last N entries."""
        if limit is not None:
            return self.history.tail(limit)
        return self.history
    
    def clear_history(self) -> None:
        """Clear all calculation history."""
        try:
            self.history = pd.DataFrame(columns=['timestamp', 'operation', 'x', 'y', 'result'])
            self._save_history()
            logger.info("Cleared calculation history")
        except Exception as e:
            logger.error(f"Error clearing history: {str(e)}")
            raise
    
    def get_statistics(self) -> Dict:
        """Calculate basic statistics about calculations."""
        try:
            stats = {
                'total_calculations': len(self.history),
                'operations_count': self.history['operation'].value_counts().to_dict(),
                'average_result': self.history['result'].mean(),
                'max_result': self.history['result'].max(),
                'min_result': self.history['result'].min()
            }
            logger.info("Generated calculation statistics")
            return stats
        except Exception as e:
            logger.error(f"Error generating statistics: {str(e)}")
            raise