from django import template
from django.db.models import Q

from core.models import Solicitacao
from django.db import models

register = template.Library()


@register.simple_tag
def get_solicitacoes_quantia(request):
    solicitacoes = solicitacoes = (
        Solicitacao.objects.filter(
            models.Q(enviado_por=request.user) | models.Q(enviado_para=request.user),
            respondida=False,
            visualizada=False,
        )
        .distinct()
        .order_by("enviado_em")
    ).count()

    return solicitacoes
