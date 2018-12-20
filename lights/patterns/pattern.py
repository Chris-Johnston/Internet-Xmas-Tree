"""
Abstract base class for patterns

"""

from abc import ABCMeta, abstractmethod

class Pattern(metaclass=ABCMeta):
    
    @abstractmethod
    def get_id(self):
        """
        Gets the pattern associated with this ID
        """
        raise NotImplementedError()

    @abstractmethod
    def update(self, strip, state):
        """
        Updates the strip with the given state
        """
        raise NotImplementedError()