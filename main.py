import sys
from calculator import Calculator
from decimal import Decimal, InvalidOperation

def calculate_and_print(a_string, b_string, operation_name):
    # a = Decimal(a)
    # b = Decimal(b)
    try:
        try:
            a = Decimal(a_string)
            b = Decimal(b_string)
        except InvalidOperation:
            print(f"Invalid number input: {a_string} or {b_string} is not a valid number.")
            return
        if operation_name == 'add':
            result = Calculator.add(a, b)
        elif operation_name == 'subtract':
            result = Calculator.subtract(a, b)
        elif operation_name == 'multiply':
            result = Calculator.multiply(a, b)
        elif operation_name == 'divide':
            result = Calculator.divide(a, b)
        else:
            result = None

        if result:
            print(f"The result of {a} {operation_name} {b} is equal to {result}")
        else:
            print(f"Unknown operation: {operation_name}")
    except InvalidOperation:
        print(f"Invalid number input: {a} or {b} is not a valid number.")
    except ZeroDivisionError:
        print("Error: Division by zero.")
    except Exception as e: # Catch-all for unexpected errors
        print(f"An error occurred: {e}")

def main():
    if len(sys.argv) != 4:
        print("Usage: python calculator_main.py <number1> <number2> <operation>")
        sys.exit(1)
    
    _, a, b, operation = sys.argv
    calculate_and_print(a, b, operation)

if __name__ == '__main__':
    main()