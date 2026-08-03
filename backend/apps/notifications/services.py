from .models import Notification


def notify(
    recipients,
    title,
    body="",
    category=Notification.Category.GENERAL,
    display_style=Notification.DisplayStyle.PERSISTENT,
    sent_by=None,
):
    """Create one Notification per recipient. `recipients` can be a
    single user or any iterable of users — used by other apps to fire
    notifications on their own events."""
    if hasattr(recipients, "pk"):
        recipients = [recipients]
    Notification.objects.bulk_create([
        Notification(
            recipient=user, title=title, body=body,
            category=category, display_style=display_style, sent_by=sent_by,
        )
        for user in recipients
    ])
