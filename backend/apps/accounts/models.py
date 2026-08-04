import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone


# ---------------------------------------------------------------------
# Branch — every member, department, group, and event hangs off this.
# ---------------------------------------------------------------------
class Branch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=255, blank=True)
    short_description = models.CharField(
        max_length=255, blank=True,
        help_text="e.g. 'Located near Samburu Primary School' — shown on the circuit/branches list.",
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    attendance_radius_meters = models.PositiveIntegerField(
        default=100,
        help_text="How close (meters) a member must be to check in on-site.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------
# Permission / Role — granular permission-based RBAC (Section 2 of spec).
# ---------------------------------------------------------------------
class Permission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(
        max_length=50, unique=True,
        help_text="e.g. youth.manage, finance.view, finance.approve, groups.manage",
    )
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return self.code


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=80, unique=True)
    is_admin = models.BooleanField(
        default=False,
        help_text="Base type flag — what they can actually do is still "
                   "controlled by individual `permissions` below.",
    )
    can_act_as_superintendent = models.BooleanField(
        default=False,
        help_text="Pastor role: steps in as acting Superintendent when the "
                   "Superintendent Minister is on leave.",
    )
    is_clergy = models.BooleanField(
        default=False,
        help_text="Included in the clergy directory (Superintendent, Pastor, "
                   "Bishop, Preacher, Evangelist, etc.).",
    )
    permissions = models.ManyToManyField(Permission, blank=True, related_name="roles")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def has_permission(self, code: str) -> bool:
        return self.permissions.filter(code=code).exists()


# ---------------------------------------------------------------------
# User — email login (no username), passport photo, branch, role.
# ---------------------------------------------------------------------
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)


class MaritalStatus(models.TextChoices):
    SINGLE = "single", "Single"
    MARRIED = "married", "Married"
    WIDOWED = "widowed", "Widowed"
    DIVORCED = "divorced", "Divorced"


class MembershipStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    TRANSFERRED = "transferred", "Transferred"


class MembershipStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    TRANSFERRED = "transferred", "Transferred"


class User(AbstractUser):
    username = None  # email is the login field, no separate username
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    passport_photo = models.ImageField(upload_to="passport_photos/", null=True, blank=True)

    membership_number = models.CharField(max_length=20, unique=True, blank=True)
    branch = models.ForeignKey(
        Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="members"
    )
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, blank=True, related_name="users"
    )

    date_of_birth = models.DateField(null=True, blank=True)
    marital_status = models.CharField(
        max_length=10, choices=MaritalStatus.choices, null=True, blank=True,
        help_text="Required for group eligibility checks, e.g. Youth = single only.",
    )
    status = models.CharField(
        max_length=15, choices=MembershipStatus.choices, default=MembershipStatus.ACTIVE,
        help_text="Current status; full change history in membership.MembershipStatusChange.",
    )
    bio = models.TextField(
        blank=True, help_text="Short bio, shown on the clergy directory if applicable."
    )

    google_sub = models.CharField(
        max_length=255, null=True, blank=True, unique=True,
        help_text="Google account subject ID, set on first 'Continue with Google' login.",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return f"{self.full_name} <{self.email}>"

    def save(self, *args, **kwargs):
        if not self.membership_number:
            self.membership_number = self._generate_membership_number()
        super().save(*args, **kwargs)

    def _generate_membership_number(self):
        # Format: MCK{year}{4-digit sequence within that year}, e.g. MCK20260011
        year = timezone.now().year
        prefix = f"MCK{year}"
        last = User.objects.filter(membership_number__startswith=prefix).order_by(
            "-membership_number"
        ).first()
        next_seq = 1
        if last and last.membership_number[len(prefix):].isdigit():
            next_seq = int(last.membership_number[len(prefix):]) + 1
        return f"{prefix}{next_seq:04d}"

    @property
    def age(self):
        if not self.date_of_birth:
            return None
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def has_permission(self, code: str) -> bool:
        if self.is_superuser:
            return True
        return bool(self.role and self.role.has_permission(code))

    # --- Section 2c: role-driven UI visibility ---
    # Maps a permission code to the home-page feature folder it unlocks.
    # Folders with no entry here (Bible, Sermons, Prayer, Counselling,
    # Attendance, Events, Catechism, Me) are available to every signed-in
    # member by default per Section 2b, so they're not gated by a code.
    FOLDER_PERMISSION_MAP = {
        "youth.manage": "Youth Registration",
        "jctm.manage": "JCTM",
        "groups.manage": "Groups",
        "finance.view": "Give (view)",
        "finance.approve": "Give (approve)",
        "finance.reports": "Finance Reports",
        "hbc.manage_members": "HBC",
        "ict.manage_content": "ICT Admin",
        "dept.manage_own": "Department Management",
        "reports.view": "Reports",
        "content.manage": "Announcements Admin",
        "members.view_all": "Member Directory",
        "sermons.manage": "Sermons Admin",
        "livestream.manage": "Livestream Admin",
        "counseling.view": "Counseling Admin",
        "leadership.manage": "Leadership Admin",
    }
    DEFAULT_MEMBER_FOLDERS = [
        "Bible", "Sermons", "Prayer Request", "Counselling Booking",
        "Sunday Attendance", "Events", "Catechism Registration", "Me",
        "Main/General Registration", "Give",
    ]

    @property
    def visible_folders(self):
        folders = list(self.DEFAULT_MEMBER_FOLDERS)
        if self.role:
            codes = set(self.role.permissions.values_list("code", flat=True))
            for code, folder in self.FOLDER_PERMISSION_MAP.items():
                if code in codes and folder not in folders:
                    folders.append(folder)
        return folders