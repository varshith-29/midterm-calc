"""Test suite for calculation history management."""

import os
import pytest
import pandas as pd
from calculator.history import CalculationHistory

@pytest.fixture
def history():
    """Fixture to create and clean up a test history instance."""
    hist = CalculationHistory("test_history.csv")
    yield hist
    # Cleanup
    if os.path.exists("test_history.csv"):
        os.remove("test_history.csv")

def test_history_initialization(history):
    """Test history manager initialization."""
    assert isinstance(history.history, pd.DataFrame)
    assert list(history.history.columns) == ['timestamp', 'operation', 'x', 'y', 'result']

def test_add_calculation(history):
    """Test adding calculations to history."""
    history.add_calculation('+', 2, 3, 5)
    assert len(history.history) == 1
    assert history.history.iloc[0]['operation'] == '+'
    assert history.history.iloc[0]['x'] == 2
    assert history.history.iloc[0]['y'] == 3
    assert history.history.iloc[0]['result'] == 5

def test_get_history(history):
    """Test retrieving history with and without limits."""
    history.add_calculation('+', 2, 3, 5)
    history.add_calculation('-', 5, 3, 2)

    full_history = history.get_history()
    assert len(full_history) == 2

    limited_history = history.get_history(limit=1)
    assert len(limited_history) == 1

def test_clear_history(history):
    """Test clearing history."""
    history.add_calculation('+', 2, 3, 5)
    history.clear_history()
    assert len(history.history) == 0

def test_get_statistics(history):
    """Test generating history statistics."""
    history.add_calculation('+', 2, 3, 5)
    history.add_calculation('+', 3, 4, 7)
    history.add_calculation('-', 5, 3, 2)

    stats = history.get_statistics()
    assert stats['total_calculations'] == 3
    assert stats['operations_count']['+'] == 2
    assert stats['operations_count']['-'] == 1
    assert stats['average_result'] == pytest.approx(4.67, rel=1e-2)
    assert stats['max_result'] == 7
    assert stats['min_result'] == 2

def test_persistence(history):
    """Test history persistence to file."""
    history.add_calculation('+', 2, 3, 5)
    history._save_history() # pylint: disable=protected-access

    new_history = CalculationHistory("test_history.csv")
    assert len(new_history.history) == 1
    assert new_history.history.iloc[0]['operation'] == '+'
