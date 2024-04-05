from django.contrib import admin
from core.models import (
    Carona,
    Caroneiro,
    Motorista,
    Avaliacao,
    Ponto,
    MetodoPagamento,
    Combinado,
    Deslocamento,
    Solicitacao,
    Temporario,
)

admin.site.register(Carona)
admin.site.register(Caroneiro)
admin.site.register(Motorista)
admin.site.register(Avaliacao)
admin.site.register(Ponto)
admin.site.register(MetodoPagamento)
admin.site.register(Combinado)
admin.site.register(Deslocamento)
admin.site.register(Solicitacao)
admin.site.register(Temporario)
