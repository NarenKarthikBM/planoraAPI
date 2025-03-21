from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

USER_ROLE_CHOICES = [("Admin", "Admin"), ("Member", "Member")]


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """This model stores the details of users
    Returns:
        class: details of users
    """

    email = models.EmailField(
        _("email address"), help_text="Email Address", unique=True, db_index=True
    )
    mobile_no = models.CharField(
        _("mobile no"),
        help_text="Mobile No",
        max_length=20,
        blank=True,
        null=True,
        db_index=True,
    )
    name = models.CharField(_("name"), help_text="Name", max_length=50, db_index=True)
    role = models.CharField(
        _("role"),
        help_text="User Role",
        max_length=10,
        choices=USER_ROLE_CHOICES,
    )
    is_staff = models.BooleanField(_("is staff"), help_text="Is Staff", default=False)
    is_superuser = models.BooleanField(
        _("is superuser"), help_text="Is Superuser", default=False
    )
    is_active = models.BooleanField(_("is active"), help_text="Is Active", default=True)
    date_joined = models.DateTimeField(
        _("date joined"), help_text="Date Joined", auto_now_add=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        """Stores Meta data of the model class"""

        verbose_name = "user"
        verbose_name_plural = "users"


class UserAuthTokens(models.Model):
    """This model stores user's auth tokens
    Returns:
        class: details of user's auth tokens
    """

    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        verbose_name="user",
        help_text="User",
        related_name="auth_tokens",
        related_query_name="auth_tokens",
    )

    auth_token = models.CharField(
        _("auth token"), help_text="Auth Token", max_length=255, unique=True, default=""
    )
    device_token = models.CharField(
        _("device token"),
        help_text="Device Token",
        max_length=255,
        unique=True,
        default="",
    )
    type = models.CharField(
        _("type"),
        help_text="Type of token",
        max_length=50,
        choices=[("web", "Web"), ("api", "API")],
    )
    created_at = models.DateTimeField(
        _("created at"), help_text="Created At", auto_now_add=True
    )
    last_used_at = models.DateTimeField(
        _("last used at"), help_text="Last Used At", null=True, blank=True
    )

    def __str__(self):
        return f"{self.user.email} - {self.type}"

    class Meta:
        verbose_name = "user auth token"
        verbose_name_plural = "user auth tokens"


class UserPermissions(models.Model):
    """This model stores additional information about user permissions
    Returns:
        class: details of user permissions
    """

    user = models.OneToOneField(
        "users.CustomUser",
        on_delete=models.CASCADE,
        verbose_name="user",
        help_text="User",
        related_name="permissions",
        related_query_name="permissions",
    )
    permissions = models.JSONField(
        _("permissions"),
        help_text="Permissions granted to the user",
        default=dict,
    )
    updated_at = models.DateTimeField(
        _("updated at"), help_text="Updated At", auto_now=True
    )
    updated_by = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        verbose_name="updated by",
        help_text="Updated By",
        null=True,
        blank=True,
        related_name="updated_permissions",
        related_query_name="updated_permissions",
    )

    def __str__(self):
        return f"{self.user.email} - Permissions"

    class Meta:
        verbose_name = "user permissions"
        verbose_name_plural = "user permissions"
