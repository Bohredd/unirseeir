from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Carona

@receiver(m2m_changed, sender=Carona.caroneiros.through)
def update_vagas(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove']:
        instance.vagas = instance.limite_vagas - instance.caroneiros.count()
        instance.save(update_fields=['vagas'])
