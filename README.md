# Command-Line Calculator

A feature-rich command-line calculator application with plugin support, calculation history management, and comprehensive logging.

## Features

- Basic arithmetic operations (add, subtract, multiply, divide)
- Memory operations for storing and recalling values
- Scientific calculator functions (power, square root)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/varshith-29/midterm-calc
   cd midterm-calc
   ```

2. Setup Virtual Environment and Install dependencies:
   ```bash
   py -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Usage

Run the calculator:
```bash
py main.py
```

### Available Commands

- Basic Operations:
  - `add X Y` - Add two numbers
  - `subtract X Y` - Subtract Y from X
  - `multiply X Y` - Multiply two numbers
  - `divide X Y` - Divide X by Y

## Testing

```bash
pytest --num_records=100
pytest --pylint --cov
```
