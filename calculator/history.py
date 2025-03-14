"""History management for calculator operations."""
from __future__ import annotations
import numpy as np
import logging
import os
import pandas as pd
from datetime import datetime
from typing import Dict, Optional, List, Any, Union

logger = logging.getLogger(__name__)

class CalculationHistory:
    """Manages calculation history using pandas DataFrame."""

    COLUMNS = ['timestamp', 'operation', 'x', 'y', 'result']

    def __init__(self, history_file: str = "calculator_history.csv") -> None:
        """Initialize history manager.
        
        Args:
            history_file: Path to history file
        """
        self.history_file = history_file
        # Use a different name for the internal DataFrame to avoid recursion
        self._df = pd.DataFrame([], columns=self.COLUMNS)
        
        try:
            self._load_history()
            logger.info("History manager initialized")
        except Exception as e:
            logger.warning(f"Could not load history: {e}")
            # Ensure we have a valid DataFrame
            self._df = pd.DataFrame([], columns=self.COLUMNS)
    
    # Add property for backward compatibility with tests
    @property
    def history(self):
        """Get the history DataFrame (for backward compatibility)."""
        return self._df
    
    @history.setter
    def history(self, value):
        """Set the history DataFrame (for backward compatibility)."""
        self._df = value

    def _load_history(self) -> None:
        """Load history from CSV file if it exists."""
        if os.path.exists(self.history_file):
            try:
                self._df = pd.read_csv(self.history_file)
                self._df['timestamp'] = pd.to_datetime(self._df['timestamp'])
                logger.info("History loaded from file")
            except Exception as e:
                logger.warning(f"Failed to load history from file: {e}")
                self._df = pd.DataFrame([], columns=self.COLUMNS)
        else:
            logger.info("No history file found")
            self._df = pd.DataFrame([], columns=self.COLUMNS)

    def add_calculation(self, operation: str, x: float, y: float, result: float) -> None:
        """Add a calculation to history.
        
        Args:
            operation: The operation performed
            x: First operand
            y: Second operand
            result: Result of calculation
            
        Raises:
            Exception: If the calculation cannot be added to history
        """
        try:
            # Check for special values
            if np.isinf(x) or np.isnan(x):
                raise ValueError("Cannot store infinite or NaN value for x")
            if np.isinf(y) or np.isnan(y):
                raise ValueError("Cannot store infinite or NaN value for y")
                
            # Create new row
            new_row = pd.DataFrame([{
                'timestamp': datetime.now(),
                'operation': operation,
                'x': x,
                'y': y,
                'result': result
            }])
            
            # Add to DataFrame
            self._df = pd.concat([self._df, new_row], ignore_index=True)
            
            # Save to file
            self._save_history()
            logger.info(f"Added calculation: {operation} {x} {y} = {result}")
        except Exception as e:
            logger.error(f"Failed to add calculation: {e}")
            raise Exception(f"Failed to save calculation: {str(e)}")

    def get_history(self, limit: Optional[int] = None) -> pd.DataFrame:
        """Get calculation history.
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            DataFrame containing calculation history
        """
        if self._df.empty:
            return pd.DataFrame([], columns=self.COLUMNS)
            
        df = self._df.sort_values('timestamp', ascending=False)
        if limit is not None and limit > 0:
            df = df.head(limit)
            
        return df

    def clear_history(self) -> None:
        """Clear calculation history."""
        try:
            self._df = pd.DataFrame([], columns=self.COLUMNS)
            
            # Remove history file if it exists
            if os.path.exists(self.history_file):
                os.remove(self.history_file)
                
            logger.info("History cleared")
        except Exception as e:
            logger.error(f"Error clearing history: {e}")
            raise Exception(f"Failed to clear history: {str(e)}")

    def get_statistics(self) -> Dict[str, Any]:
        """Calculate statistics about calculations.
        
        Returns:
            Dict containing calculation statistics
            
        Raises:
            Exception: If there is an error calculating statistics
        """
        if self._df.empty:
            return {
                'total_calculations': 0,
                'operations_count': {},
                'average_result': 0.0,
                'max_result': float('-inf'),
                'min_result': float('inf')
            }

        try:
            # Ensure numeric operations are safe
            stats = {
                'total_calculations': len(self._df),
                'operations_count': dict(self._df['operation'].value_counts())
            }
            
            # Handle special values
            results = pd.to_numeric(self._df['result'], errors='coerce')
            finite_results = results[~np.isinf(results)]
            valid_results = finite_results[~np.isnan(finite_results)]

            if len(valid_results) == 0:
                stats.update({
                    'average_result': 0.0,
                    'max_result': float('-inf'),
                    'min_result': float('inf')
                })
            else:
                stats.update({
                    'average_result': float(valid_results.mean()),
                    'max_result': float(valid_results.max()),
                    'min_result': float(valid_results.min())
                })

            return stats

        except Exception as e:
            logger.error(f"Error calculating statistics: {e}")
            raise Exception(f"Failed to calculate statistics: {str(e)}")

    def _save_history(self) -> None:
        """Save history to CSV file.
        
        Raises:
            Exception: If file cannot be written
            IOError: If there is an IO error during save
        """
        try:
            self._df.to_csv(self.history_file, index=False)
            logger.debug("History saved to file")
        except Exception as e:
            logger.error(f"Error saving history: {e}")
            raise Exception(f"Failed to save history to file: {str(e)}")