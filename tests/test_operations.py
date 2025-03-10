'''Test arithmetic operations'''
# test_operations.py
from decimal import Decimal
import pytest
from calculator.operations import addition, subtraction, multiplication, division

# pylint: disable=invalid-name
def test_operation(a, b, operation, expected):  # Keep original names used by parametrize
    '''Testing each arithmetic operation'''
    first_num = Decimal(a)  # Use better names in the function body
    second_num = Decimal(b)
    expected = Decimal(expected)
    if operation == 'add':
        calculation = addition(first_num, second_num)
    elif operation == 'subtract':
        calculation = subtraction(first_num, second_num)
    elif operation == 'multiply':
        calculation = multiplication(first_num, second_num)
    elif operation == 'divide':
        calculation = division(first_num, second_num)
    else:
        calculation = Decimal(0)
    assert calculation == expected, f"{operation} operation failed"

def test_divide_by_zero():
    '''Testing the divide by zero exception'''
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        division(Decimal('10'), Decimal('0'))
