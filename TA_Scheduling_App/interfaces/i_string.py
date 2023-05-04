from abc import abstractmethod
from django.db import models

from TA_Scheduling_App.utils.abc_model_meta import ABCModelMeta

class IString(models.Model, metaclass=ABCModelMeta):
    class Meta:
        abstract = True

    @abstractmethod
    def checkString(self):
        pass