from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from django.contrib.auth.models import Group


@receiver(post_save, sender=User)
def create_user_group(sender, instance, created, **kwargs):
    groups = None  # Inicializar groups con un valor predeterminado
    if created:
        try:
            groups = Group.objects.get(name='Customer')
        except Group.DoesNotExist:
            # Si el grupo no existe, crealo
            groups = Group.objects.create(name='Customer')

    if groups:
        instance.groups.add(groups)
