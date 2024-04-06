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


class CaroneiroAdmin(admin.ModelAdmin):
    list_display = ("nome", "matricula", "user")


admin.site.register(Caroneiro, CaroneiroAdmin)


class CaronaAdmin(admin.ModelAdmin):
    list_display = (
        "get_motorista_nome",
        "vagas",
        "limite_vagas",
        "get_caroneiros_nomes",
    )

    def get_motorista_nome(self, obj):
        return obj.motorista.nome

    def get_caroneiros_nomes(self, obj):
        return ", ".join([caroneiro.nome for caroneiro in obj.caroneiros.all()])

    get_caroneiros_nomes.short_description = "Caroneiros"

    get_motorista_nome.short_description = "Motorista"


admin.site.register(Carona, CaronaAdmin)

admin.site.register(Motorista)
admin.site.register(Avaliacao)
admin.site.register(Ponto)
admin.site.register(MetodoPagamento)
admin.site.register(Combinado)
admin.site.register(Deslocamento)
admin.site.register(Solicitacao)
admin.site.register(Temporario)
