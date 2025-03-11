"""Test suite for core calculator functionality."""

import pytest
from calculator.core import Calculator

def test_calculator_initialization():
    """Test calculator initialization and operations dictionary."""
    calc = Calculator()
    assert set(calc.operations.keys()) == {'+', '-', '*', '/'}

def test_add():
    """Test addition operation."""
    calc = Calculator()
    assert calc.add(2, 3) == 5
    assert calc.add(-1, 1) == 0
    assert calc.add(0.1, 0.2) == pytest.approx(0.3)

def test_subtract():
    """Test subtraction operation."""
    calc = Calculator()
    assert calc.subtract(5, 3) == 2
    assert calc.subtract(1, -1) == 2
    assert calc.subtract(0.3, 0.1) == pytest.approx(0.2)

def test_multiply():
    """Test multiplication operation."""
    calc = Calculator()
    assert calc.multiply(2, 3) == 6
    assert calc.multiply(-2, 3) == -6
    assert calc.multiply(0.1, 0.2) == pytest.approx(0.02)

def test_divide():
    """Test division operation."""
    calc = Calculator()
    assert calc.divide(6, 2) == 3
    assert calc.divide(-6, 2) == -3
    assert calc.divide(0.3, 0.1) == pytest.approx(3.0)

def test_divide_by_zero():
    """Test division by zero raises ValueError."""
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.divide(5, 0)

def test_calculate():
    """Test calculate method with various operations."""
    calc = Calculator()
    assert calc.calculate('+', 2, 3) == 5
    assert calc.calculate('-', 5, 3) == 2
    assert calc.calculate('*', 2, 3) == 6
    assert calc.calculate('/', 6, 2) == 3

def test_invalid_operation():
    """Test invalid operation raises ValueError."""
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.calculate('^', 2, 3)