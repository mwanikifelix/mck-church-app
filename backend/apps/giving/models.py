from django.conf import settings
from django.db import models


class Donation(models.Model):
    """A gift made through the official church paybill (as opposed to
    HBCContribution, which is money paid directly to an HBC's own
    treasurer number and never touches the church paybill).

    If hbc_group is set, this donation was deposited via the CHURCH
    paybill but tagged by the depositor/recorder as being on behalf of
    that HBC — e.g. an HBC treasurer banking collected cash through the
    official paybill rather than holding it personally. It still counts
    as official church money (visible to church treasurer/admin) AND
    counts toward that HBC's totals.
    """

    class AccountCode(models.TextChoices):
        TITHE = "T", "Tithe"
        OFFERING = "O", "Offering"
        PLEDGE = "P", "Pledge"
        BUILDING_FUND = "B", "Building Fund"
        EDUCATION = "E", "Education"
        HARVEST = "H", "Harvest"
        GENERAL = "G", "General"

    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="donations",
    )
    account_code = models.CharField(max_length=1, choices=AccountCode.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    phone = models.CharField(max_length=20, blank=True)
    mpesa_ref = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=200, blank=True)

    hbc_group = models.ForeignKey(
        "hbc.HBCGroup",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="church_paybill_donations",
        help_text=(
            "Set only if this was deposited via the church paybill on "
            "behalf of a specific HBC (e.g. by that HBC's treasurer). "
            "Null = ordinary giving, not tied to any HBC."
        ),
    )

    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="donations_recorded",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_account_code_display()} {self.amount} - {self.member}"


class Paybill(models.Model):
    """The single active church-wide paybill number. Kept as its own
    tiny table (rather than a settings constant) so it can be updated
    from the admin/API without a deploy if the number ever changes."""

    number = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.number
