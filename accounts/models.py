from django.db import models
import uuid
from django.contrib import admin
from django.core.validators import MaxValueValidator, MinValueValidator, EmailValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from datetime import date
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError(_("Email is required."))
        username = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("phone", 0000000000)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        return self.create_user(username, password, **extra_fields)


class Users(AbstractUser):
    id = models.UUIDField(primary_key=True,null = False, unique=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=1000)
    email = models.EmailField(blank=False, unique=True, validators=[EmailValidator,])
    password = models.CharField(max_length=5000)
    phone = models.BigIntegerField(blank=False, unique=False, validators=[MaxValueValidator(9999999999)])
    otp = models.CharField(max_length=100, null=True, editable=False)
    profile = models.ImageField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_subscribed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','password','phone']
    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff
    
    def get_all_permissions(user=None):
        if user.is_staff:
            return set()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return str(self.email)

class Cards(models.Model):
    uid = models.ForeignKey(Users, on_delete=models.CASCADE, blank=False)
    number = models.PositiveBigIntegerField(blank=False, unique=False, validators=[MaxValueValidator(999999999999)])
    month = models.PositiveIntegerField(blank=False, unique=False, validators=[MinValueValidator(1), MaxValueValidator(12)])
    year = models.PositiveIntegerField(blank=False, unique=False, validators=[MinValueValidator(date.today().year)])
    code = models.PositiveIntegerField(blank=False, unique=False, validators=[MaxValueValidator(999)])

    class Meta:
        verbose_name = "Card"
        verbose_name_plural = "Cards"
    
    def __str__(self):
        return str(self.number)