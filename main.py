"""Calculator REPL entry point."""
from calculator.repl import CalculatorREPL
from calculator.config import logger

def main():
    logger.info("Starting calculator application")
    repl = CalculatorREPL()
    repl.run()
    logger.info("Calculator application terminated")

if __name__ == '__main__':
    main()