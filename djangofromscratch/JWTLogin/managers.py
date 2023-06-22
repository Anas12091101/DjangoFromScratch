import re

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as DjangoUserManager


class UserManager(DjangoUserManager):
    # Define a function for
    # for validating an Email
    def check_email(self, email):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"

        # pass the regular expression
        # and the string into the fullmatch() method
        if re.fullmatch(regex, email):
            return True
        return False

    def check_password(self, password):
        special_re = re.compile("[@_!#$%^&*()<>?/\|}{~:]")
        if (
            len(password) >= 8
            and special_re.search(password) != None
            and bool(re.search(r"\d", password))
        ):
            return True
        return False

    def _create_user(self, email: str, password: str | None, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        if not self.check_password(password):
            raise ValueError(
                "Password should be atleast 8 characters long with a number and special character in it"
            )
        if not self.check_email(email):
            raise ValueError("Enter a valid email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
