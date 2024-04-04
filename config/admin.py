from django.contrib import admin
from config.models import Config, Mensagem, Conversa, Conexao

admin.site.register(Config)
admin.site.register(Mensagem)
admin.site.register(Conversa)
admin.site.register(Conexao)