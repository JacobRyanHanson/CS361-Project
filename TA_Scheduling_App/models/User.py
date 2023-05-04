import string
import datetime
import re

from django.db import models
from abc import ABCMeta
from ..interfaces.i_string import IString
from django.db.models.base import ModelBase

# Used so that the constructor can distinguish between no input Null()
# and 'None' given explicitly as input.
from TA_Scheduling_App.utils.null import Null


class User(IString):
    USER_ID = models.AutoField(primary_key=True)
    ROLE = models.CharField(max_length=10)
    FIRST_NAME = models.CharField(max_length=255)
    LAST_NAME = models.CharField(max_length=255)
    EMAIL = models.EmailField(unique=True)
    PASSWORD_HASH = models.CharField(max_length=255)
    PHONE_NUMBER = models.CharField(max_length=20)
    ADDRESS = models.CharField(max_length=255)
    BIRTH_DATE = models.DateField()
    SKILLS = models.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        passwordHash = kwargs.get('PASSWORD_HASH', Null())

        if passwordHash is None or (not isinstance(passwordHash, str) and not Null()):
            raise ValueError("Invalid password")

        if passwordHash is not Null():
            self.PASSWORD_HASH = passwordHash

        if not self.setRole(kwargs.get('ROLE', Null())):
            raise ValueError("Invalid role")

        if not self.setFirstName(kwargs.get('FIRST_NAME', Null())):
            raise ValueError("Invalid first name")

        if not self.setLastName(kwargs.get('LAST_NAME', Null())):
            raise ValueError("Invalid last name")

        if not self.setEmail(kwargs.get('EMAIL', Null())):
            raise ValueError("Invalid email")

        if not self.setPhoneNumber(kwargs.get('PHONE_NUMBER', Null())):
            raise ValueError("Invalid phone number")

        if not self.setAddress(kwargs.get('ADDRESS', Null())):
            raise ValueError("Invalid address")

        if not self.setBirthDate(kwargs.get('BIRTH_DATE', Null())):
            raise ValueError("Invalid birth date")

    def setRole(self, role):
        if role is Null():
            return True

        if role in ["ADMIN", "INSTRUCTOR", "TA"]:
            self.ROLE = role
            return True
        return False

    def setFirstName(self, firstName):
        if firstName is Null():
            return True

        result = self.checkString(firstName, False)
        if result is False:
            return False

        self.FIRST_NAME = firstName
        return True

    def setLastName(self, lastName):
        if lastName is Null():
            return True

        result = self.checkString(lastName, False)
        if result is False:
            return False

        self.LAST_NAME = lastName
        return True

    def setEmail(self, email):
        if email is Null():
            return True

        # Regular expression for email validation with TLD
        pattern = r'^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$'

        # Check if email is None or longer than 255 characters
        if email is None or len(email) > 255:
            return False

        # Check if the email address matches the pattern
        if not re.match(pattern, email):
            return False

        self.EMAIL = email
        return True

    def setPhoneNumber(self, phoneNumber):
        if phoneNumber is Null():
            return True

        # This pattern matches phone numbers in the format xxx-xxx-xxxx, xxx xxx xxxx, or xxxxxxxxxx
        pattern = r'^\d{3}[ -]?\d{3}[ -]?\d{4}$'

        # Check if email is None or longer than 255 characters
        if phoneNumber is None or len(phoneNumber) > 20:
            return False

        # Check if the email address matches the pattern
        if not re.match(pattern, phoneNumber):
            return False

        self.PHONE_NUMBER = phoneNumber
        return True

    def setAddress(self, address):
        if address is Null():
            return True

        if address is None:
            return False

        new_address = address.strip()

        if not new_address:
            return False

        if len(new_address) > 255:
            return False

        if not all(c.isascii() for c in new_address):
            return False

        if not any(c.isalnum() for c in new_address):
            return False

        self.ADDRESS = new_address
        return True

    def setBirthDate(self, birthDate):
        if birthDate is Null():
            return True

        if not isinstance(birthDate, datetime.date):
            return False

        # Check if the birthDate is not in the future
        if birthDate > datetime.date.today():
            return False

        # If all checks pass, set the birthdate
        self.BIRTH_DATE = birthDate
        return True

    def checkString(self, value, allowPartialNumeric=True, allowEmpty=False):
        if (value is None or not isinstance(value, str) or not value.strip()) and not allowEmpty:
            return False

        # For empty strings, return True if they are allowed
        if allowEmpty and (value is None or not value.strip()):
            return True

        # Trim whitespace from beginning and end of string
        value = value.strip()

        # Check that string is not too long
        if len(value) > 255:
            return False

        # Ensure the string is not completely numeric
        if value.isdigit():
            return False

        # Check that string contains only alphanumeric characters, spaces, and certain punctuation marks
        allowed_chars = set(string.ascii_letters + (string.digits if allowPartialNumeric else "") + " -'.:,")
        if not all(c in allowed_chars for c in value):
            return False

        return value