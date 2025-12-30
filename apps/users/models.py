from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import EmailValidator


class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        if not phone_number:
            raise ValueError("Номер телефона обязателен")

        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        if not password:
            raise ValueError("Пароль обязателен для суперпользователя")

        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        user = self.create_user(email, phone_number, password=password, **extra_fields)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        verbose_name="Email",
    )
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        verbose_name="Номер телефона",
    )
    first_name = models.CharField(max_length=50, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=50, blank=True, verbose_name="Фамилия")

    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_staff = models.BooleanField(default=False, verbose_name="Доступ в админку")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number"]

    objects = UserManager()

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    # для профиля (карточки)
    goals_achieved = models.PositiveIntegerField(default=0)   # "Цель достигнута"
    saving_days = models.PositiveIntegerField(default=0)      # "Дней экономии"

    # настройки экрана (по желанию, но удобно)
    notifications_enabled = models.BooleanField(default=True)
    theme = models.CharField(max_length=10, default="system")  # light/dark/system
    language = models.CharField(max_length=5, default="ru")    # ru/ky/en

    def __str__(self):
        return f"Profile of {self.user.email}"

class Privilege(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    def __str__(self):
        return self.name


class UserPrivilege(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    privilege = models.ForeignKey(Privilege, on_delete=models.CASCADE, verbose_name="Привилегия")
    purchased_at = models.DateTimeField(auto_now_add=True, verbose_name="Куплено")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "privilege"], name="uniq_user_privilege")
        ]
        verbose_name = "Привилегия пользователя"
        verbose_name_plural = "Привилегии пользователей"

    def __str__(self):
        return f"{self.user.email} - {self.privilege.name}"
