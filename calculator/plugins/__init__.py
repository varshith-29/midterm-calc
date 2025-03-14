"""Plugin system for calculator."""

# Expose plugin registration functions
# Note: Import the specific register_commands from each plugin
from calculator.plugins.memory import register_commands as register_memory_commands  
from calculator.plugins.scientific import register_commands as register_scientific_commands

# Expose key functions
__all__ = [
    'register_memory_commands',
    'register_scientific_commands',
]