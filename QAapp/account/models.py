from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
import uuid
from django import forms
class AccountManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, dob, password=None):
        if not email:
            raise forms.ValueError("User must have email")
        if not username:
            raise forms.ValueError("User must have username")
        if not first_name:
            raise forms.ValueError("User must have first_name")
        if not last_name:
            raise forms.ValueError("User must have last_name")
        if not dob:
            raise forms.ValueError("User must have dob")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            dob = dob
        )
        
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, dob, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            dob = dob,
            password = password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user
        

class Account(AbstractUser):
    id = models.UUIDField(editable=False, unique=True, primary_key=True, default=uuid.uuid4)
    email = models.EmailField(verbose_name='email', unique=True, max_length=60)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    dob = models.DateTimeField(auto_now_add=False, null=False)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'dob']

    def __str__(self):
        return "Email: " + str(self.email)

    def has_perm(self, perm, obj=None):
        if self.is_admin:
            return True
        else:
            return False

    def has_module_perms(self, app_label):
        return True
