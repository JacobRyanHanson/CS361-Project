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