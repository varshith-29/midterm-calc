"""Test suite for calculator commands."""
from decimal import Decimal
import pytest
from calculator.commands.arithmetic import (
    AddCommand,
    SubtractCommand,
    MultiplyCommand,
    DivideCommand
)

@pytest.mark.parametrize("command_class,a,b,expected", [
    (AddCommand, Decimal('5'), Decimal('3'), Decimal('8')),
    (SubtractCommand, Decimal('10'), Decimal('4'), Decimal('6')),
    (MultiplyCommand, Decimal('6'), Decimal('7'), Decimal('42')),
    (DivideCommand, Decimal('15'), Decimal('3'), Decimal('5')),
])
def test_command_execute(command_class, a, b, expected):
    """Test command execution with various operations."""
    command = command_class()
    result = command.execute(a, b)
    assert result == expected

def test_divide_by_zero():
    """Test division by zero handling."""
    command = DivideCommand()
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        command.execute(Decimal('10'), Decimal('0'))

@pytest.mark.parametrize("command_class,expected_text", [
    (AddCommand, "Add two numbers (Usage: add number1 number2)"),
    (SubtractCommand, "Subtract two numbers (Usage: subtract number1 number2)"),
    (MultiplyCommand, "Multiply two numbers (Usage: multiply number1 number2)"),
    (DivideCommand, "Divide two numbers (Usage: divide number1 number2)"),
])
def test_command_description(command_class, expected_text):
    """Test command descriptions."""
    assert command_class.description() == expected_text
