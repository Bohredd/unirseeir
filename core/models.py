from django.db import models
from django.db.models import TextChoices
from core.utils import verificar_matricula_valida, obter_qr_code_pix
from django.contrib.auth.models import User


class Automovel(TextChoices):
    carro = ("carro", "Carro")
    moto = ("moto", "Moto")


quantia_vagas_total = {
    "carro": 4,
    "moto": 1,
}


class AvaliacaoTipos(TextChoices):

    motorista = ("motorista", "Motorista")
    caroneiro = ("caroneiro", "Caroneiro")


class Avaliacao(models.Model):

    nota = models.PositiveSmallIntegerField()
    quem_avaliou = models.IntegerField(verbose_name="ID de quem Avaliou")
    tipo_avaliacao = models.CharField(
        choices=AvaliacaoTipos.choices,
        max_length=30,
    )
    descricao = models.CharField(max_length=200)


def get_upload_path(instance, filename):
    return f"files/carona/{instance.nome_remetente}/comprovantes/{filename}"


class Ponto(models.Model):
    nome = models.CharField(max_length=150, verbose_name="Ponto de Encontro")
    x = models.CharField(
        max_length=25, verbose_name="Coordenada X do ponto de encontro"
    )
    y = models.CharField(
        max_length=25, verbose_name="Coordenada Y do ponto de encontro"
    )


class Metodos(TextChoices):

    pix = (
        "pix",
        "PIX",
    )


class MetodoPagamento(models.Model):

    nome = models.CharField(choices=Metodos.choices, max_length=20)
    chave = models.CharField(max_length=100)


class Motorista(models.Model):
    nome = models.CharField(max_length=200)
    matricula = models.CharField(max_length=20)
    comprovante = models.FileField(upload_to=get_upload_path)
    ponto_saida = models.ForeignKey(Ponto, on_delete=models.CASCADE)
    curso = models.CharField(max_length=100)
    automovel = models.CharField(
        max_length=200, verbose_name="Qual o automóvel dirigido:"
    )
    carona_paga = models.BooleanField(
        verbose_name="Precisa pagar pela carona?", default=True
    )

    pagamento = models.ForeignKey(MetodoPagamento, on_delete=models.CASCADE)

    custo = models.FloatField(verbose_name="Custo pela carona", default=0.0)
    horario_saida = models.CharField(
        max_length=10, verbose_name="Horário de Saída para o Destino"
    )
    horario_volta = models.CharField(
        max_length=10, verbose_name="Horário de Volta para o Ponto de Saída"
    )
    matricula_valida = models.BooleanField(default=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):

        self.matricula_valida = verificar_matricula_valida(self.comprovante, self)
        print("Resultado do self.matricula_valida = ", self.matricula_valida)
        super().save(*args, **kwargs)


class Caroneiro(models.Model):
    nome = models.CharField(max_length=200)
    matricula = models.CharField(max_length=20)
    comprovante = models.FileField(upload_to=get_upload_path)
    ponto_encontro = models.ForeignKey(Ponto, on_delete=models.CASCADE)
    curso = models.CharField(max_length=100)
    matricula_valida = models.BooleanField(default=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):

        self.matricula_valida = verificar_matricula_valida(self.comprovante, self)
        print("Resultado do self.matricula_valida = ", self.matricula_valida)
        super().save(*args, **kwargs)


class Carona(models.Model):
    motorista = models.ForeignKey(
        Motorista, related_name="Motorista", on_delete=models.CASCADE
    )
    tipo = models.CharField(
        choices=Automovel.choices,
        max_length=50,
    )
    vagas = models.IntegerField(default=0)
    limite_vagas = models.IntegerField(default=0)
    caroneiros = models.ManyToManyField(
        Caroneiro, verbose_name="Alunos que estão pegando carona"
    )
    ativa = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.tipo in quantia_vagas_total:
            self.limite_vagas = quantia_vagas_total[self.tipo]
            self.ativa = True
            self.update_vagas()
        super().save(*args, **kwargs)

    def update_vagas(self, *args, **kwargs):
        self.vagas = self.limite_vagas - self.caroneiros.count()
        super().save(*args, **kwargs)

    def generate_pix(self, *args, **kwargs):
        print("Gerando contratos: ", *args, **kwargs)

        return obter_qr_code_pix()

    def get_caroneiros_nomes(self, template=False):

        caroneiros = list(self.caroneiros.all().values_list("nome", flat=True))

        if len(caroneiros) > 1:

            if template:
                string = "os caroneiros "
                for idx, caroneiro in enumerate(caroneiros):
                    if idx == len(caroneiros) - 1:
                        string += " e " + caroneiro + "."
                        string = string.replace(",  e", " e")
                    else:
                        string += caroneiro + ", "

                return string

        if template:
            return "o caroneiro ".join(caroneiros) + "."
        else:
            return caroneiros
