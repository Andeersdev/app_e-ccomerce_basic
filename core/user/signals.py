from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from django.contrib.auth.models import Group


@receiver(post_save, sender=User)
def create_user_group(sender, instance, created, **kwargs):
    if created:
        groups = Group.objects.get(name='Customer')
    else:
        groups = Group.objects.create(name='Customer')
    instance.groups.add(groups)
