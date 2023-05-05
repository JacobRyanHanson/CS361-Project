from abc import ABCMeta
from django.db.models.base import ModelBase


# Class to resolve inheritance
class ABCModelMeta(ABCMeta, ModelBase):
    pass