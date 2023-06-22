import re

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.db.models import CharField, EmailField
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_rest_passwordreset.signals import reset_password_token_created

from .managers import UserManager


# reset_password_token_created signal triggers this fn
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "Hi user, you have initiated a reset password requests. Here's your token for it: token={}".format(
        reset_password_token.key
    )
    email = EmailMessage(
        "DnagoFromScratch _ Password Reset Request",
        email_plaintext_message,
        "muhammad.anas@arbisoft.com",
        [reset_password_token.user.email],
        reply_to=["muhammad.anas@arbisoft.com"],
        headers={"Message-ID": "foo"},
    )
    email.send(fail_silently=False)


def check_email(email):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"

    # pass the regular expression
    # and the string into the fullmatch() method
    if re.fullmatch(regex, email):
        return True
    raise ValidationError("Enter a valid Email")


def check_password(password):
    special_re = re.compile("[@_!#$%^&*()<>?/\|}{~:]")
    if (
        len(password) >= 8
        and special_re.search(password) != None
        and bool(re.search(r"\d", password))
    ):
        return True
    raise ValidationError(
        "Password should be atleast 8 characters long with a number and special character in it"
    )


class User(AbstractUser):
    """
    Default custom user model for SimpleLogin.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    email = EmailField(_("email address"), unique=True, validators=[check_email])
    username = None  # type: ignore

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super(User, self).save(*args, **kwargs)
        except IntegrityError:
            raise ValidationError("error message")
