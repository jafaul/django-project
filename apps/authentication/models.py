from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import gettext_lazy as _


class SchoolUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('position', User.Position.ADMIN)
        user = self.create_user(email, password, **extra_fields)

        admin_group, created = Group.objects.get_or_create(name="Admin")
        user.groups.add(admin_group)

        return user


class User(AbstractUser):
    class Position(models.TextChoices):
        ADMIN = "admin", _("Admin")
        MANAGER = "manager", _("Manager")
        TEACHER = "teacher", _("Teacher")
        STUDENT = "student", _("Student")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    email = models.EmailField(_('email address'), unique=True)
    objects = SchoolUserManager()
    position = models.CharField(max_length=20, choices=Position.choices, default=Position.STUDENT)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super(User, self).save(*args, **kwargs)

        group, _ = Group.objects.get_or_create(name=self.position)

        self.groups.clear()
        self.groups.add(group)

    @property
    def is_staff(self):
        return self.position in {User.Position.TEACHER, User.Position.ADMIN}

    @property
    def is_superuser(self):
        return self.position == User.Position.ADMIN
