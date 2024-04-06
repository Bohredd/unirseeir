from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from .models import Carona, Caroneiro


@receiver(m2m_changed, sender=Carona.caroneiros.through)
def update_vagas(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove"]:
        if instance.vagas != 0:
            instance.vagas = instance.limite_vagas - instance.caroneiros.count()
            instance.save(update_fields=["vagas"])
        else:
            if instance.caroneiros.count() == 0 and instance.vagas == 0:
                instance.vagas = instance.limite_vagas
                instance.save(update_fields=["vagas"])


@receiver(m2m_changed, sender=Carona.caroneiros.through)
def check_vagas_disponiveis(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add':
        carona = instance
        if carona.vagas + 1 < carona.caroneiros.count():
            ultimo_adicionado = carona.caroneiros.last()
            carona.caroneiros.remove(ultimo_adicionado)
            carona.save()

@receiver(pre_save, sender=Carona)
def set_limite_vagas(sender, instance, **kwargs):

    quantia_vagas_total = {
        "carro": 4,
        "moto": 1,
    }

    if instance.tipo in quantia_vagas_total:
        instance.limite_vagas = quantia_vagas_total[instance.tipo]
        try:
            instance.vagas = instance.limite_vagas - instance.caroneiros.count()
        except ValueError:
            instance.vagas = instance.limite_vagas
