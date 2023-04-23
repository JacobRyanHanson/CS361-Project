from abc import ABC, abstractmethod

class IVerification(ABC):

    @abstractmethod
    def checkDuplicate(self):
        pass
