"""Main entry point for calculator application."""
import logging
import sys
from calculator.repl import CalculatorREPL
from calculator.config import setup_logging

logger = logging.getLogger(__name__)

def main() -> int:
    """Main entry point for the calculator REPL.
    
    Returns:
        0 for successful exit, 1 for error
    """
    try:
        # Initialize logging
        setup_logging()
        
        # Create and configure REPL
        repl = CalculatorREPL()
        repl.intro = "Simple Calculator. Type 'help' for a list of commands."
        
        # Start command loop
        try:
            logger.info("Starting calculator REPL")
            repl.cmdloop()
            logger.info("Calculator REPL exited normally")
            return 0
        except KeyboardInterrupt:
            print("\nGoodbye!")
            logger.info("Calculator terminated by keyboard interrupt")
            return 0
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            print(f"An unexpected error occurred: {e}")
            return 1
    except Exception as e:
        print(f"Failed to initialize calculator: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())