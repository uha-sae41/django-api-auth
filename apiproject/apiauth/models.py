from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, nom, prenom, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est requis")
        email = self.normalize_email(email)
        user = self.model(email=email, nom=nom, prenom=prenom, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, nom, prenom, password=None, **extra_fields):
        extra_fields.setdefault('role', 'administrateur')
        return self.create_user(email, nom, prenom, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('administrateur', 'Administrateur'),
        ('banquier', 'Banquier'),
        ('client', 'client'),
    ]

    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=150)
    date_creation = models.DateTimeField(default=timezone.now)
    dernier_login = models.DateTimeField(null=True, blank=True)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='client')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']

    objects = CustomUserManager()

    def __str__(self):
        return self.email