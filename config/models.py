from django.db import models
from django.contrib.auth.models import User


class Config(models.Model):

    semestre = models.PositiveSmallIntegerField()
    ano = models.PositiveSmallIntegerField()


class Mensagem(models.Model):

    enviado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    conteudo = models.TextField()
    enviado_em = models.DateTimeField(auto_now_add=True)
    visualizado = models.BooleanField(default=False)

    def send_message(self, conexao):
        if conexao.ativa:
            conversa = Conversa.objects.filter(
                conexoes=conexao,
                membros=self.enviado_por,
            )

            print(conexao)
            print(self.enviado_por)

            print("CONVERSA")
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
        Mensagem,
        blank=True,
    )

    membros = models.ManyToManyField(User)

    conexoes = models.ManyToManyField(
        Conexao,
        blank=True,
    )

    def get_conversa_formatada(self):

        mensagens = list(
            self.mensagens.order_by("enviado_em").values_list("conteudo", "enviado_por")
        )

        print(mensagens)

        return mensagens

    def get_usuarios_conversa(self):

        if self.membros.count() == 2:
            return " e ".join(self.membros.all().values_list("first_name", flat=True))
        else:
            return " e ".join(self.membros.all().values_list("first_name", flat=True))

    def get_membros(self):
        return list(self.membros.all().values_list("first_name", flat=True))


class CoordenadaCEP(models.Model):

    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)

    cep = models.CharField(max_length=50)

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
