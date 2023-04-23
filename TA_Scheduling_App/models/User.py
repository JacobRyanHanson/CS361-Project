import datetime
from django.db import models


class User(models.Model):
    USER_ID = models.AutoField(primary_key=True)
    ROLE = models.CharField(max_length=10, choices=(('ADMIN', 'Admin'), ('INSTRUCTOR', 'Instructor'), ('TA', 'Teaching Assistant')))
    FIRST_NAME = models.CharField(max_length=255)
    LAST_NAME = models.CharField(max_length=255)
    EMAIL = models.EmailField(unique=True)
    PASSWORD_HASH = models.CharField(max_length=255)
    PHONE_NUMBER = models.CharField(max_length=20)
    ADDRESS = models.CharField(max_length=255)
    BIRTH_DATE = models.DateField()

    def setBirthDate(self, birthDate):
        if not isinstance(birthDate, datetime.date):
            return False

        # Check if the birthDate is not in the future
        if birthDate > datetime.date.today():
            return False

        # If all checks pass, set the birth date
        self.BIRTH_DATE = birthDate
        return True
    