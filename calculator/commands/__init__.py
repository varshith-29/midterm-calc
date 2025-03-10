"""Command pattern implementation for calculator operations."""
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict, Type

class Command(ABC):
    """Base command interface."""
    
    @abstractmethod
    def execute(self, *args) -> Decimal:
        """Execute the command with given arguments."""
        pass
    
    @classmethod
    @abstractmethod
    def description(cls) -> str:
        """Return description of what the command does."""
        pass