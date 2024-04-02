from django.db import models
from django.db.models import TextChoices

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
    quem_avaliou = models.IntegerField(verbose_name='ID de quem Avaliou')
    tipo_avaliacao = models.CharField(
        choices=AvaliacaoTipos.choices,
        max_length=30,
    )
    descricao = models.CharField(
        max_length=200
    )

def get_upload_path(instance, filename):
    return f"files/carona/{instance.name}/comprovantes/{filename}"


class Ponto(models.Model):
    nome = models.CharField(max_length=150, verbose_name="Ponto de Encontro")
    x = models.CharField(max_length=25, verbose_name="Coordenada X do ponto de encontro")
    y = models.CharField(max_length=25, verbose_name="Coordenada Y do ponto de encontro")

class Motorista(models.Model):
    nome = models.CharField(max_length=200)
    matricula = models.CharField(max_length=20)
    comprovante = models.FileField(upload_to=get_upload_path)
    ponto_saida = models.ForeignKey(Ponto, on_delete=models.CASCADE)
    curso = models.CharField(max_length=100)
    automovel = models.CharField(max_length=200, verbose_name="Qual o automóvel dirigido:")
    carona_paga = models.BooleanField(verbose_name="Precisa pagar pela carona?", default=True)
    custo = models.FloatField(verbose_name="Custo pela carona", default=0.0)
    horario_saida = models.TimeField(verbose_name="Horário de Saída para o Destino")
    horario_volta = models.TimeField(verbose_name="Horário de Volta para o Ponto de Saída")
    matricula_valida = models.BooleanField(default=True)

    def save(self, *args, **kwargs):

        print("vai verificar matricula is valida")
        super().save(*args, **kwargs)

class Caroneiro(models.Model):
    nome = models.CharField(max_length=200)
    matricula = models.CharField(max_length=20)
    comprovante = models.FileField(upload_to=get_upload_path)
    ponto_encontro = models.ForeignKey(Ponto, on_delete=models.CASCADE)
    curso = models.CharField(max_length=100)
    matricula_valida = models.BooleanField(default=True)

    def save(self, *args, **kwargs):

        print("vai verificar matricula is valida")
        super().save(*args, **kwargs)

class Carona(models.Model):
    motorista = models.ForeignKey(Motorista, related_name="Motorista", on_delete=models.CASCADE)
    tipo = models.CharField(
        choices=Automovel.choices,
        max_length=50,
    )
    vagas = models.IntegerField(default=0)
    limite_vagas = models.IntegerField(default=0)
    caroneiros = models.ManyToManyField(
        Caroneiro, verbose_name="Alunos que estão pegando carona", null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if self.tipo in quantia_vagas_total:
            self.limite_vagas = quantia_vagas_total[self.tipo]
        super().save(*args, **kwargs)

    def update_vagas(self, *args, **kwargs):
        self.vagas = self.limite_vagas - self.caroneiros.count()
        super().save(*args, **kwargs)

    def generate_contrato(self, *args, **kwargs):
        print("Gerando contratos: ", *args, **kwargs)

        if self.motorista.carona_paga:
            price_per_caroneiro = self.motorista.custo
        else:
            price_per_caroneiro = 0

