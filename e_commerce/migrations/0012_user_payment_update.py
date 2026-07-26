from django.db import migrations
from django.db.models import F, Q


def update_subscription_payment_date(apps, schema_editor):
    """
    Updates User.subscription_payment_update with created_at date from UserSubscriberMapping
    if a mapping exists for the user.
    """
    User = apps.get_model('e_commerce', 'User')  # Replace 'your_app_name' with actual app name
    UserSubscriberMapping = apps.get_model('core', 'UserSubscriberMapping')

    # Get all users that have a mapping
    users_with_mapping = UserSubscriberMapping.objects.values('user_id', 'created_at')

    # Update users one by one
    updated_count = 0
    skipped_count = 0

    for user in User.objects.all():
        # Find the mapping for this user
        mapping = next(
            (m for m in users_with_mapping if m['user_id'] == user.id),
            None
        )

        if mapping:
            user.subscription_payment_update = mapping['created_at']
            user.save()
            updated_count += 1
        else:
            user.subscription_payment_update=user.created_at
            user.save()
            skipped_count += 1

    print(f"Migration complete: {updated_count} users updated, {skipped_count} users skipped")


def reverse_subscription_payment_date(apps, schema_editor):
    """
    Reverses the update by setting subscription_payment_update to None
    """
    User = apps.get_model('e_commerce', 'User')
    User.objects.update(subscription_payment_update=None)


class Migration(migrations.Migration):
    dependencies = [
        ('e_commerce', '0011_user_subscription_payment_update'),  # Replace with actual previous migration
    ]

    operations = [
        migrations.RunPython(
            update_subscription_payment_date,
            reverse_subscription_payment_date
        ),
    ]