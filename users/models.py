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
    email_verified = models.BooleanField(
        _("email verified"), help_text="Email Verified", default=False
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
    location = models.CharField(
        _("location"),
        help_text="Location",
        max_length=50,
        blank=True,
        null=True,
    )
    latitude = models.DecimalField(
        _("latitude"),
        help_text="Latitude",
        max_digits=9,
        decimal_places=5,
        blank=True,
        null=True,
    )
    longitude = models.DecimalField(
        _("longitude"),
        help_text="Longitude",
        max_digits=9,
        decimal_places=5,
        blank=True,
        null=True,
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


class UserVerificationOTP(models.Model):
    """This model stores user's verification OTP
    Returns:
        class: details of user's verification OTP
    """

    email = models.EmailField(
        _("email"),
        help_text="Email",
        db_index=True,
    )
    otp = models.CharField(
        _("otp"),
        help_text="OTP",
        max_length=6,
    )
    created_at = models.DateTimeField(
        _("created at"), help_text="Created At", auto_now_add=True
    )

    def __str__(self):
        return self.email

    class Meta:
        """Stores Meta data of the model class"""

        verbose_name = "user verification otp"
        verbose_name_plural = "user verification otps"


class Organisation(models.Model):
    """This model stores the details of organisations
    Returns:
        class: details of organisations
    """

    name = models.CharField(
        _("name"), help_text="Name", max_length=100, db_index=True, unique=True
    )
    logo = models.ImageField(
        _("logo"), help_text="Logo", upload_to="organisations/", blank=True, null=True
    )
    description = models.TextField(
        _("description"), help_text="Description", blank=True
    )
    email = models.EmailField(
        _("contact email"),
        help_text="Contact Email",
        db_index=True,
    )
    tags = models.JSONField(
        _("tags"),
        help_text="Tags",
        default=list,
    )
    committee = models.ManyToManyField(
        "users.CustomUser",
        verbose_name=_("committee"),
        help_text="Committee Members",
        through="users.OrganisationCommittee",
        through_fields=("organisation", "user"),
        related_name="organisations",
        related_query_name="organisation",
        blank=True,
    )
    location = models.CharField(
        _("location"),
        help_text="Location",
        max_length=100,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        _("created at"), help_text="Created At", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("updated at"), help_text="Updated At", auto_now=True
    )

    def __str__(self):
        return self.name

    class Meta:
        """Stores Meta data of the model class"""

        verbose_name = "organisation"
        verbose_name_plural = "organisations"


class OrganisationCommittee(models.Model):
    """This model stores the details of organisation committee
    Returns:
        class: details of organisation committee
    """

    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        verbose_name="user",
        help_text="User",
        related_name="organisation_committee",
        related_query_name="organisation_committee",
    )
    organisation = models.ForeignKey(
        "users.Organisation",
        on_delete=models.CASCADE,
        verbose_name="organisation",
        help_text="Organisation",
        related_name="committee_members",
        related_query_name="committee_member",
    )
    designation = models.CharField(
        _("designation"),
        help_text="Designation",
        max_length=50,
        default="Member",
    )
    permissions = models.JSONField(
        _("permissions"),
        help_text="Permissions granted to the user",
        default=dict,
    )
    created_at = models.DateTimeField(
        _("created at"), help_text="Created At", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("updated at"), help_text="Updated At", auto_now=True
    )

    def __str__(self):
        return f"{self.user.email} - {self.organisation.name}"

    class Meta:
        """Stores Meta data of the model class"""

        verbose_name = "organisation committee"
        verbose_name_plural = "organisation committees"


class UserPreference(models.Model):
    """This model stores user designation, preferences, and email notification settings"""

    user = models.OneToOneField(
        "users.CustomUser",
        on_delete=models.CASCADE,
        verbose_name=_("user"),
        help_text="User",
        related_name="preferences",
    )

    # Designation
    designation = models.CharField(_("designation"), help_text="User Designation", max_length=255)

    # Preferred Categories (Multiple Choices)
    preferred_categories = models.CharField(_("preferred_category"),help_text="Category",max_length=50,choices=categories)

    # Email Notification Preferences
    allow_marketing_emails = models.BooleanField(_("marketing emails"), help_text="Allow Marketing Emails", default=True)
    allow_event_updates = models.BooleanField(_("event updates"), help_text="Allow Event Updates", default=True)
    allow_system_notifications = models.BooleanField(_("system notifications"), help_text="Allow System Notifications", default=True)

    # Timestamps
    created_at = models.DateTimeField(_("created at"), help_text="Created At", auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), help_text="Updated At", auto_now=True)

    class Meta:
        verbose_name = _("User Preference")
        verbose_name_plural = _("User Preferences")

    def __str__(self):
        return f"Preferences of {self.user.name}"