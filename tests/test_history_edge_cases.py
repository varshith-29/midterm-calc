"""Additional test suite for history edge cases and error handling."""
import os
import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from calculator.history import CalculationHistory

@pytest.fixture
def history():
    """Test fixture for history testing."""
    test_file = "test_history_edge.csv"
    # Clean up before test
    if os.path.exists(test_file):
        os.remove(test_file)
    yield CalculationHistory(test_file)
    # Clean up after test
    if os.path.exists(test_file):
        os.remove(test_file)

def test_load_corrupted_file(tmp_path):
    """Test loading a corrupted history file."""
    # Create a corrupted CSV file
    corrupted_file = tmp_path / "corrupted.csv"
    with open(corrupted_file, "w") as f:
        f.write("This is not a valid CSV file")
    
    # Should handle corrupted file gracefully
    history = CalculationHistory(str(corrupted_file))
    assert isinstance(history.get_history(), pd.DataFrame)
    assert len(history.get_history()) == 0

def test_save_to_readonly_location(tmp_path):
    """Test saving history to a read-only location."""
    if os.name == 'nt':  # Skip on Windows
        pytest.skip("Chmod not fully supported on Windows")
    
    read_only_dir = tmp_path / "readonly"
    read_only_dir.mkdir()
    read_only_file = read_only_dir / "history.csv"
    
    # Make directory read-only
    os.chmod(read_only_dir, 0o444)
    try:
        history = CalculationHistory(str(read_only_file))
        # Should handle save error gracefully
        history.add_calculation("add", 1, 2, 3)
        assert len(history.get_history()) == 1
    finally:
        os.chmod(read_only_dir, 0o755)

def test_save_error_handling(history, monkeypatch):
    """Test error handling during save operation."""
    def mock_to_csv(*args, **kwargs):
        raise IOError("Mock save error")
    
    # Mock DataFrame.to_csv to raise an error
    monkeypatch.setattr(pd.DataFrame, "to_csv", mock_to_csv)
    
    # Should handle save error gracefully
    history.add_calculation("add", 1, 2, 3)
    assert len(history.get_history()) == 1

def test_statistics_with_empty_history(history):
    """Test statistics calculation with empty history."""
    stats = history.get_statistics()
    assert stats["total_calculations"] == 0
    assert stats["operations_count"] == {}
    assert stats["average_result"] == 0
    assert stats["max_result"] == float("-inf")
    assert stats["min_result"] == float("inf")

def test_statistics_with_single_value(history):
    """Test statistics calculation with a single value."""
    history.add_calculation("add", 1, 2, 3)
    stats = history.get_statistics()
    assert stats["total_calculations"] == 1
    assert stats["operations_count"]["add"] == 1
    assert stats["average_result"] == 3
    assert stats["max_result"] == 3
    assert stats["min_result"] == 3

def test_load_history_file_permission_error(tmp_path):
    """Test loading history with insufficient permissions."""
    if os.name == 'nt':  # Skip on Windows
        pytest.skip("Chmod not fully supported on Windows")
    
    no_access_dir = tmp_path / "noaccess"
    no_access_dir.mkdir()
    history_file = no_access_dir / "history.csv"
    
    # Create file and make directory inaccessible
    history_file.touch()
    os.chmod(no_access_dir, 0o000)
    try:
        history = CalculationHistory(str(history_file))
        assert isinstance(history.get_history(), pd.DataFrame)
        assert len(history.get_history()) == 0
    finally:
        os.chmod(no_access_dir, 0o755)

def test_add_calculation_with_special_values():
    """Test adding calculations with special values."""
    history = CalculationHistory()
    
    # Test with infinity
    with pytest.raises(Exception):
        history.add_calculation('+', float('inf'), 1.0, float('inf'))
    
    # Test with NaN
    with pytest.raises(Exception):
        history.add_calculation('+', float('nan'), 1.0, float('nan'))
    
    # Test with very large number (should work)
    history.add_calculation('+', 1.0, 10000000000.0, 10000000000.0)
    stats = history.get_statistics()
    assert stats['max_result'] == 10000000000.0

def test_add_calculation_error():
    """Test error handling in add_calculation."""
    history = CalculationHistory()
    
    # Mock _save_history to raise an exception
    with patch.object(CalculationHistory, '_save_history', side_effect=Exception("Mock save error")):
        with pytest.raises(Exception):
            history.add_calculation('+', 1.0, 2.0, 3.0)

def test_clear_history_error():
    """Test error handling in clear_history."""
    history = CalculationHistory()
    
    # Mock os.remove to raise an exception
    with patch('os.remove', side_effect=Exception("Mock remove error")):
        # Add a calculation to ensure there's a file to remove
        history.add_calculation('+', 1.0, 2.0, 3.0)
        
        with pytest.raises(Exception):
            history.clear_history()

def test_get_statistics_error():
    """Test error handling in get_statistics."""
    history = CalculationHistory()
    
    # Mock pd.to_numeric to raise an exception
    with patch('pandas.to_numeric', side_effect=Exception("Mock stats error")):
        # Add a calculation to ensure there's data
        history.add_calculation('+', 1.0, 2.0, 3.0)
        
        with pytest.raises(Exception):
            history.get_statistics()

def test_save_history_error():
    """Test error handling in _save_history."""
    history = CalculationHistory()
    
    # Mock DataFrame.to_csv to raise an exception
    with patch.object(pd.DataFrame, 'to_csv', side_effect=Exception("Mock save error")):
        with pytest.raises(Exception):
            history._save_history()

def test_edge_case_data_types():
    """Test handling of edge case data types."""
    history = CalculationHistory()
    
    # Test with large integers
    history.add_calculation('+', 1.0, 10000000000.0, 10000000000.0)
    
    # Get statistics and check values
    stats = history.get_statistics()
    assert stats['max_result'] == 10000000000.0

def test_statistics_with_invalid_results(history):
    """Test statistics calculation with invalid/special results."""
    # Add mix of normal and special values
    history.add_calculation("add", 1, 2, 3)
    history.add_calculation("add", float("inf"), 1, float("inf"))
    history.add_calculation("add", float("nan"), 1, float("nan"))
    
    stats = history.get_statistics()
    # Should handle inf/nan gracefully in statistics
    assert not pd.isna(stats["total_calculations"])
    assert stats["total_calculations"] == 3