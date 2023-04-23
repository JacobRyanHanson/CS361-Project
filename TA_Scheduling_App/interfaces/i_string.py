from abc import ABC, abstractmethod
from django.db import models

class IString(ABC):
    @abstractmethod
    def checkString(self):
        pass
