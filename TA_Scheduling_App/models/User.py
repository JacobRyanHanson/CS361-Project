import string
import datetime
import re
from email_validator import validate_email, EmailNotValidError

from django.db import models


class User(models.Model):
    USER_ID = models.AutoField(primary_key=True)
    ROLE = models.CharField(max_length=10,
                            choices=(('ADMIN', 'Admin'), ('INSTRUCTOR', 'Instructor'), ('TA', 'Teaching Assistant')))
    FIRST_NAME = models.CharField(max_length=255)
    LAST_NAME = models.CharField(max_length=255)
    EMAIL = models.EmailField(unique=True)
    PASSWORD_HASH = models.CharField(max_length=255)
    PHONE_NUMBER = models.CharField(max_length=20)
    ADDRESS = models.CharField(max_length=255)
    BIRTH_DATE = models.DateField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setRole(self, role):
        if role in ["ADMIN", "INSTRUCTOR", "TA"]:
            self.role = role
            return True
        return False

    def checkString(self, value, allowPartialNumeric=True, allowEmpty=False, max=255, special_chars=""):
        if (value is None or not isinstance(value, str) or not value.strip()) and not allowEmpty:
            return False

        if allowEmpty and (value is None or not value.strip()):
            return True

        if value.strip() != value:
            return False

        if len(value) > max:
            return False

        if value.isdigit():
            return False

        allowed_chars = set(string.ascii_letters + (string.digits if allowPartialNumeric else "") + " -'.:," + special_chars)
        if not all(c in allowed_chars or (c.isalnum() and not c.isascii()) for c in value):
            return False

        return value

    def checkDuplicate(self, email):
        return User.objects.filter(EMAIL=email).exists()

    def setFirstName(self, firstName):
        firstName = self.checkString(firstName, False)
        if firstName is False:
            return False

        self.FIRST_NAME = firstName
        return True

    def setLastName(self, lastName):
        lastName = self.checkString(lastName, False)
        if lastName is False:
            return False

        self.LAST_NAME = lastName
        return True

    def setEmail(self, email):
        if email is None:
            return False

        try:
            validate_email(email)
        except EmailNotValidError:
            return False

        if self.checkDuplicate(email):
            return False

        self.EMAIL = email
        return True

    def setPhoneNumber(self, phoneNumber, region=None):
        if phoneNumber is None or not isinstance(phoneNumber, str) or not phoneNumber.strip():
            return False

        if len(phoneNumber) > 20:
            return False

        pattern = re.compile(
            r"^(?:\+\d{1,3}\s?)?[-. (]*\d{1,4}[-. )]*(\d{1,3}[-. ]*){1,2}\d{1,4}$"
        )

        if not pattern.match(phoneNumber):
            return False

        self.phoneNumber = phoneNumber
        return True

    def setAddress(self, address):
        address = self.checkString(address, special_chars="()\n#")
        if address is False:
            return False

        self.ADDRESS = address
        return True

    def setBirthDate(self, birthDate):
        if not isinstance(birthDate, datetime.date):
            return False

        # Check if the birthDate is not in the future
        if birthDate > datetime.date.today():
            return False

        # If all checks pass, set the birthdate
        self.BIRTH_DATE = birthDate
        return True

