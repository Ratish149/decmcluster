from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model for Vanuatu CIM.
    Extend this model with additional fields as required by the application.
    """

    def __str__(self):
        return self.username
