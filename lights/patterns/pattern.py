"""
Abstract base class for patterns

"""

from abc import ABCMeta, abstractmethod

class Pattern(metaclass=ABCMeta):
    
    @abstractmethod
    def get_id():
        """
        Gets the pattern associated with this ID
        """
        pass


    @abstractmethod
    def update(strip, state):
        """
        Updates the strip with the given state
        """
        pass