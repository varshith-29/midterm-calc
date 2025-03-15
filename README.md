# Advanced Python Calculator

A feature-rich command-line calculator application with plugin support, calculation history management, and comprehensive logging.

## Features

- Basic arithmetic operations (add, subtract, multiply, divide)
- Calculation history management using Pandas
- Plugin system for extending functionality
- Professional logging system
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
   py -m venv .venv     #for windows
   python -m venv venv  #for MacOs
   ```
   ```bash
   .venv\Scripts\activate   #for windows
   source venv/bin/activate #for MacOS
   ```
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the calculator:
```bash
py -m calculator
```

### Available Commands

- Basic Operations:
  - `add X Y` - Add two numbers
  - `subtract X Y` - Subtract Y from X
  - `multiply X Y` - Multiply two numbers
  - `divide X Y` - Divide X by Y

- History Management:
  - `history [limit]` - Show calculation history
  - `stats` - Show calculation statistics
  - `clear` - Clear calculation history

- Plugin Commands:
  - Scientific Calculator:
    - `pow X Y` - Calculate X raised to power Y
    - `sqrt X` - Calculate square root of X
  - Memory Operations:
    - `store NAME VALUE` - Store a value in memory
    - `recall NAME` - Recall a value from memory
    - `clear_memory` - Clear all stored memory values
    - `memory` - List all stored memory values

- System Commands:
  - `help` - Show available commands
  - `quit` - Exit the calculator

## Architecture

### Design Patterns

1. Command Pattern
   - Implemented in the REPL interface where each command is a separate method
   - Enables easy addition of new commands through plugins

2. Facade Pattern
   - Calculator class provides a simplified interface to complex operations
   - Handles logging, history management, and core calculations

3. Plugin System
   - Dynamically loads plugins from the plugins directory
   - Allows extending functionality without modifying core code

### Logging Strategy

- Environment variable configuration:
  - `CALCULATOR_LOG_LEVEL`: Set logging level (default: INFO)
  - `CALCULATOR_LOG_FILE`: Set log file path (default: calculator.log)

- Log message categories:
  - INFO: Normal operations and calculations
  - WARNING: Non-critical issues
  - ERROR: Critical errors and exceptions

### Data Management

- Uses Pandas for efficient data handling
- Stores calculation history in CSV format
- Provides statistical analysis of calculations

## Testing

Run the test suite:
```bash
pytest tests/
```

Generate coverage report:
```bash
pytest --cov=calculator tests/
```
### Demo Video
[📹 Click to View](https://drive.google.com/file/d/1V0Zokpub8DfO6-XRDH8s0fTLIF5TqYQt/view?usp=sharing)
