from django.db.models.fields.files import FileField
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


def get_file_fields(instance):
    """
    Return all FileField/ImageField values for a model instance.
    """
    for field in instance._meta.fields:
        if isinstance(field, FileField):
            yield field.name, getattr(instance, field.name)


@receiver(post_delete)
def delete_files_on_instance_delete(sender, instance, **kwargs):
    """
    Delete all associated files from storage when an object is deleted.
    Works with Azure, S3, local storage, etc.
    """
    # Ignore Django internal models
    if sender._meta.app_label in ("admin", "auth", "contenttypes", "sessions"):
        return

    for _, file in get_file_fields(instance):
        if file:
            try:
                file.delete(save=False)
            except Exception:
                # Optional: log the exception
                pass


@receiver(pre_save)
def delete_old_files_on_change(sender, instance, **kwargs):
    """
    Delete old files from storage when they are replaced.
    """
    if sender._meta.app_label in ("admin", "auth", "contenttypes", "sessions"):
        return

    if not instance.pk:
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    for field_name, new_file in get_file_fields(instance):
        old_file = getattr(old_instance, field_name)

        if old_file and new_file and old_file.name != new_file.name:
            try:
                old_file.delete(save=False)
            except Exception:
                # Optional: log the exception
                pass
