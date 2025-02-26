from abc import ABC, abstractmethod
from tc_python import System

class BaseCalculator(ABC):
    """
    This class is the base class for all calculators.
    """
    def __init__(self, system: System):
        self.system = system
        
    @abstractmethod
    def calculate(self, **kwargs):
        """
        This method is used to calculate the results.
        """
        pass