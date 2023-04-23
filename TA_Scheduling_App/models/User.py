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

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     passwordHash = kwargs.get('PASSWORD_HASH', None)
    #
    #     if passwordHash is not None:
    #         if not isinstance(passwordHash, str):
    #             raise ValueError("Invalid password")
    #     else:
    #         # Prevent user from being saved to DB
    #         passwordHash = None
    #
    #     if not self.setRole(kwargs.get('ROLE', None)):
    #         raise ValueError("Invalid role")
    #
    #     if not self.setFirstName(kwargs.get('FIRST_NAME', None)):
    #         raise ValueError("Invalid first name")
    #
    #     if not self.setLastName(kwargs.get('LAST_NAME', None)):
    #         raise ValueError("Invalid last name")
    #
    #     if not self.setEmail(kwargs.get('EMAIL', None)):
    #         raise ValueError("Invalid email")
    #
    #     if not self.setPasswordHash(passwordHash):
    #         raise ValueError("Invalid password hash")
    #
    #     if not self.setPhoneNumber(kwargs.get('PHONE_NUMBER', None)):
    #         raise ValueError("Invalid phone number")
    #
    #     if not self.setAddress(kwargs.get('ADDRESS', None)):
    #         raise ValueError("Invalid address")
    #
    #     if not self.setBirthDate(kwargs.get('BIRTH_DATE', None)):
    #         raise ValueError("Invalid birth date")
    #
    #     self.PASSWORD_HASH = passwordHash

    def setBirthDate(self, birthDate):
        if not isinstance(birthDate, datetime.date):
            return False

        # Check if the birthDate is not in the future
        if birthDate > datetime.date.today():
            return False

        # If all checks pass, set the birth date
        self.BIRTH_DATE = birthDate
        return True
