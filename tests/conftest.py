'''Conftest'''
# conftest.py
from decimal import Decimal
from faker import Faker
fake = Faker()

def generate_test_data(num_records):
    '''Generate test data'''

    operations = ['add', 'subtract', 'multiply', 'divide']
    # Generate test data
    for _ in range(num_records):
        a = Decimal(fake.random_number(digits=2))
        b = Decimal(fake.random_number(digits=2)) if _ % 4 != 3 else Decimal(fake.random_number(digits=1))
        operation_name = fake.random_element(elements=operations)
        operation_func = operation_name
        # Ensure b is not zero for divide operation to prevent division by zero in expected calculation
        if operation_func == 'divide':
            b = Decimal('1') if b == Decimal('0') else b
        try:
            if operation_func == 'divide' and b == Decimal('0'):
                expected = "ZeroDivisionError"
            else:
                # Calculate expected based on operation
                if operation_func == 'add':
                    expected = a + b
                elif operation_func == 'subtract':
                    expected = a - b
                elif operation_func == 'multiply':
                    expected = a * b
                else:  # divide
                    expected = a / b
        except ZeroDivisionError:
            expected = "ZeroDivisionError"
        yield a, b, operation_name, operation_func, expected

def pytest_addoption(parser):
    '''Command line'''
    parser.addoption("--num_records", action="store", default=5, type=int, help="Number of test records to generate")

def pytest_generate_tests(metafunc):
    '''Pytest generate tests'''
    # Check if the test is expecting any of the dynamically generated fixtures
    if {"a", "b", "expected"}.intersection(set(metafunc.fixturenames)):
        num_records = metafunc.config.getoption("num_records")
        parameters = list(generate_test_data(num_records))
        # Modify parameters to fit test functions' expectations
        modified_parameters = [(a, b, op_name if 'operation_name' in metafunc.fixturenames else op_func, expected) for a, b, op_name, op_func, expected in parameters]
        metafunc.parametrize("a,b,operation,expected", modified_parameters)
