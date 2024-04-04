from django.db import models
from django.contrib.auth.models import User

class Config(models.Model):

    semestre = models.PositiveSmallIntegerField()
    ano = models.PositiveSmallIntegerField()

class Mensagem(models.Model):

    enviado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    conteudo = models.TextField()
    enviado_em = models.DateTimeField(auto_now_add=True)

    def send_message(self, conexao):
        if conexao.ativa:
            conversa = Conversa.objects.filter(
                conexoes=conexao,
                membros=self.enviado_por,
            )

            print(conversa)

            if conversa.exists():

                print("conversa exists")

                conversa.first().mensagens.add(
                    self,
                )



class Conexao(models.Model):

    ativa = models.BooleanField(default=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

class Conversa(models.Model):

    mensagens = models.ManyToManyField(
        Mensagem, blank=True,
    )

    membros = models.ManyToManyField(
        User
    )

    conexoes = models.ManyToManyField(
        Conexao, blank=True,
    )

    def get_conversa_formatada(self):

        mensagens = list(self.mensagens.order_by('enviado_em').values_list('conteudo', 'enviado_por'))

        print(mensagens)

        return mensagens