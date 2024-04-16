import datetime

from django.db import models
from django.db.models import TextChoices
from django.shortcuts import redirect, reverse
from core.utils import verificar_matricula_valida, obter_qr_code_pix, get_address_by_cep
from django.contrib.auth.models import User
from django.contrib import messages


class Cursos(TextChoices):

    ESCOLHA = "Escolha um Curso", "Escolha um Curso"
    ABI_ARTES_CENICAS = "ABI - Artes Cênicas", "ABI - Artes Cênicas"
    ABI_CIENCIAS_BIOLOGICAS = (
        "ABI - Ciências Biológicas",
        "ABI - Ciências Biológicas",
    )
    ADMINISTRACAO = "Administração", "Administração"
    AGRONEGOCIO = "Agronegócio", "Agronegócio"
    AGRONOMIA = "Agronomia", "Agronomia"
    ALIMENTOS = "Alimentos", "Alimentos"
    ARQUITETURA_E_URBANISMO = "Arquitetura e Urbanismo", "Arquitetura e Urbanismo"
    ARQUIVOLOGIA = "Arquivologia", "Arquivologia"
    ARTES_CENICAS_DIRECAO_TEATRAL = (
        "Artes Cênicas - Direção Teatral",
        "Artes Cênicas - Direção Teatral",
    )
    ARTES_CENICAS_INTERPRETACAO_TEATRAL = (
        "Artes Cênicas - Interpretação Teatral",
        "Artes Cênicas - Interpretação Teatral",
    )
    ARTES_VISUAIS = "Artes Visuais", "Artes Visuais"
    CIENCIA_DA_COMPUTACAO = "Ciência da Computação", "Ciência da Computação"
    CIENCIAS_BIOLOGICAS = "Ciências Biológicas", "Ciências Biológicas"
    CIENCIAS_CONTABEIS = "Ciências Contábeis", "Ciências Contábeis"
    CIENCIAS_ECONOMICAS = "Ciências Econômicas", "Ciências Econômicas"
    CIENCIAS_SOCIAIS = "Ciências Sociais", "Ciências Sociais"
    COMUNICACAO_SOCIAL_PRODUCAO_EDITORIAL = (
        "Comunicação Social - Produção Editorial",
        "Comunicação Social - Produção Editorial",
    )
    COMUNICACAO_SOCIAL_PUBLICIDADE_PROPAGANDA = (
        "Comunicação Social - Publicidade e Propaganda",
        "Comunicação Social - Publicidade e Propaganda",
    )
    COMUNICACAO_SOCIAL_RELACOES_PUBLICAS = (
        "Comunicação Social - Relações Públicas",
        "Comunicação Social - Relações Públicas",
    )
    DANCA_BACHARELADO = "Dança - Bacharelado", "Dança - Bacharelado"
    DANCA_LICENCIATURA = "Dança - Licenciatura", "Dança - Licenciatura"
    DESENHO_INDUSTRIAL = "Desenho Industrial", "Desenho Industrial"
    DIREITO = "Direito", "Direito"
    EDUCACAO_ESPECIAL = "Educação Especial", "Educação Especial"
    EDUCACAO_FISICA = "Educação Física", "Educação Física"
    ELETRONICA_INDUSTRIAL = "Eletrônica Industrial", "Eletrônica Industrial"
    ENFERMAGEM = "Enfermagem", "Enfermagem"
    ENGENHARIA_ACUSTICA = "Engenharia Acústica", "Engenharia Acústica"
    ENGENHARIA_AEROESPACIAL = "Engenharia Aeroespacial", "Engenharia Aeroespacial"
    ENGENHARIA_AMBIENTAL_SANITARIA = (
        "Engenharia Ambiental e Sanitária",
        "Engenharia Ambiental e Sanitária",
    )
    ENGENHARIA_CIVIL = "Engenharia Civil", "Engenharia Civil"
    ENGENHARIA_ELETRICA = "Engenharia Elétrica", "Engenharia Elétrica"
    ENGENHARIA_FLORESTAL = "Engenharia Florestal", "Engenharia Florestal"
    ENGENHARIA_MECANICA = "Engenharia Mecânica", "Engenharia Mecânica"
    ENGENHARIA_QUIMICA = "Engenharia Química", "Engenharia Química"
    ENGENHARIA_COMPUTACAO = "Engenharia da Computação", "Engenharia da Computação"
    ENGENHARIA_CONTROLE_AUTOMACAO = (
        "Engenharia de Controle e Automação",
        "Engenharia de Controle e Automação",
    )
    ENGENHARIA_PRODUCAO = "Engenharia de Produção", "Engenharia de Produção"
    ENGENHARIA_TELECOMUNICACOES = (
        "Engenharia de Telecomunicações",
        "Engenharia de Telecomunicações",
    )
    ESTATISTICA = "Estatística", "Estatística"
    FABRICACAO_MECANICA = "Fabricação Mecânica", "Fabricação Mecânica"
    FARMACIA = "Farmácia", "Farmácia"
    FILOSOFIA = "Filosofia", "Filosofia"
    FISIOTERAPIA = "Fisioterapia", "Fisioterapia"
    FONOAUDIOLOGIA = "Fonoaudiologia", "Fonoaudiologia"
    FISICA = "Física", "Física"
    GEOGRAFIA = "Geografia", "Geografia"
    GEOPROCESSAMENTO = "Geoprocessamento", "Geoprocessamento"
    GESTAO_AMBIENTAL = "Gestão Ambiental", "Gestão Ambiental"
    GESTAO_COOPERATIVAS = "Gestão de Cooperativas", "Gestão de Cooperativas"
    GESTAO_TURISMO = "Gestão de Turismo", "Gestão de Turismo"
    HISTORIA = "História", "História"
    JORNALISMO = "Jornalismo", "Jornalismo"
    LETRAS_ESPANHOL = "Letras - Espanhol", "Letras - Espanhol"
    LETRAS_INGLES = "Letras - Inglês", "Letras - Inglês"
    LETRAS_LINGUA_PORTUGUESA = (
        "Letras - Língua Portuguesa",
        "Letras - Língua Portuguesa",
    )
    LETRAS_PORTUGUES = "Letras - Português", "Letras - Português"
    MATEMATICA = "Matemática", "Matemática"
    MEDICINA = "Medicina", "Medicina"
    MEDICINA_VETERINARIA = "Medicina Veterinária", "Medicina Veterinária"
    METEOROLOGIA = "Meteorologia", "Meteorologia"
    MUSICA = "Música", "Música"
    MUSICA_TECNOLOGIA = "Música e Tecnologia", "Música e Tecnologia"
    NUTRICAO = "Nutrição", "Nutrição"
    NAO_CONSTA = "Não Consta", "Não Consta"
    ODONTOLOGIA = "Odontologia", "Odontologia"
    PEDAGOGIA = "Pedagogia", "Pedagogia"
    PROCESSOS_QUIMICOS = "Processos Químicos", "Processos Químicos"
    PROGRAMA_ESPECIAL_GRADUACAO_FORMACAO_PROFESSORES_EDUCACAO_PROFISSIONAL = (
        "Programa Especial de Graduação de Formação de Professores para A Educação Profissional",
        "Programa Especial de Graduação de Formação de Professores para A Educação Profissional",
    )
    PSICOLOGIA = "Psicologia", "Psicologia"
    QUIMICA = "Química", "Química"
    QUIMICA_INDUSTRIAL = "Química Industrial", "Química Industrial"
    REDES_COMPUTADORES = "Redes de Computadores", "Redes de Computadores"
    RELACOES_INTERNACIONAIS = "Relações Internacionais", "Relações Internacionais"
    SERVICO_SOCIAL = "Serviço Social", "Serviço Social"
    SISTEMAS_INFORMACAO = "Sistemas de Informação", "Sistemas de Informação"
    SISTEMAS_INTERNET = "Sistemas para Internet", "Sistemas para Internet"
    TEATRO = "Teatro", "Teatro"
    TERAPIA_OCUPACIONAL = "Terapia Ocupacional", "Terapia Ocupacional"
    ZOOTECNIA = "Zootecnia", "Zootecnia"


def get_upload_path(instance, filename):
    if isinstance(instance, Caroneiro) or isinstance(instance, Motorista):
        return f"files/carona/{instance.user.username}/comprovantes/{filename}"

    return f"files/carona/{instance.matricula}/comprovantes/{filename}"


class Automovel(TextChoices):
    carro = ("carro", "Carro")
    moto = ("moto", "Moto")


class TipoUsuario(TextChoices):

    caroneiro = ("caroneiro", "Caroneiro")
    motorista = ("motorista", "Motorista")


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
        verbose_name="Quem foi avaliado é o que:",
    )
    avaliado = models.IntegerField(verbose_name="ID de quem foi Avaliado")
    descricao = models.CharField(max_length=200)


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

    nome = models.CharField(
        choices=Metodos.choices, max_length=20, null=True, blank=True
    )
    chave = models.CharField(max_length=100, null=True, blank=True)


class DiasSemana(TextChoices):

    segunda = ("segunda", "Segunda")
    terca = ("terça", "Terça")
    quarta = ("quarta", "Quarta")
    quinta = ("quinta", "Quinta")
    sexta = ("sexta", "Sexta")


class Deslocamento(models.Model):

    dia_semana = models.CharField(
        choices=DiasSemana.choices,
        max_length=20,
    )
    horario_saida_ponto_saida = models.TimeField()
    ponto_saida = models.ForeignKey(
        Ponto,
        on_delete=models.CASCADE,
        related_name="deslocamentos_saida",
        null=True,
        blank=True,
    )
    ponto_destino = models.ForeignKey(
        Ponto,
        on_delete=models.CASCADE,
        related_name="deslocamentos_destino",
        null=True,
        blank=True,
    )

    ponto_saida_endereco = models.CharField(
        max_length=250,
    )

    ponto_destino_endereco = models.CharField(
        max_length=250,
    )

    cep = models.CharField(
        max_length=30,
    )


class Temporario(models.Model):

    nome = models.CharField(max_length=200)
    matricula = models.CharField(max_length=20)
    comprovante = models.FileField(upload_to=get_upload_path)
    curso = models.CharField(max_length=200, choices=Cursos.choices)
    from_username = models.CharField(max_length=100)


class EstadoChoices(TextChoices):
    ACRE = ("AC", "Acre")
    ALAGOAS = ("AL", "Alagoas")
    AMAPA = ("AP", "Amapá")
    AMAZONAS = ("AM", "Amazonas")
    BAHIA = ("BA", "Bahia")
    CEARA = ("CE", "Ceará")
    DISTRITO_FEDERAL = ("DF", "Distrito Federal")
    ESPIRITO_SANTO = ("ES", "Espírito Santo")
    GOIAS = ("GO", "Goiás")
    MARANHAO = ("MA", "Maranhão")
    MATO_GROSSO = ("MT", "Mato Grosso")
    MATO_GROSSO_DO_SUL = ("MS", "Mato Grosso do Sul")
    MINAS_GERAIS = ("MG", "Minas Gerais")
    PARA = ("PA", "Pará")
    PARAIBA = ("PB", "Paraíba")
    PARANA = ("PR", "Paraná")
    PERNAMBUCO = ("PE", "Pernambuco")
    PIAUI = ("PI", "Piauí")
    RIO_DE_JANEIRO = ("RJ", "Rio de Janeiro")
    RIO_GRANDE_DO_NORTE = ("RN", "Rio Grande do Norte")
    RIO_GRANDE_DO_SUL = ("RS", "Rio Grande do Sul")
    RONDONIA = ("RO", "Rondônia")
    RORAIMA = ("RR", "Roraima")
    SANTA_CATARINA = ("SC", "Santa Catarina")
    SAO_PAULO = ("SP", "São Paulo")
    SERGIPE = ("SE", "Sergipe")
    TOCANTINS = ("TO", "Tocantins")


class Cidade(models.Model):

    pais = models.CharField(max_length=30)
    estado = models.CharField(choices=EstadoChoices.choices, max_length=30)
    cidade = models.CharField(max_length=100)


class Endereco(models.Model):
    cep = models.CharField(max_length=30)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(choices=EstadoChoices.choices, max_length=30)
    logradouro = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    numero = models.IntegerField()
    complemento = models.CharField(max_length=100)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )


class Motorista(models.Model):
    nome = models.CharField(max_length=200)
    matricula = models.CharField(max_length=20, unique=True)
    comprovante = models.FileField(upload_to=get_upload_path)

    curso = models.CharField(max_length=200, choices=Cursos.choices)

    automovel = models.CharField(
        max_length=200, verbose_name="Qual o automóvel dirigido:"
    )
    carona_paga = models.BooleanField(
        verbose_name="Precisa pagar pela carona?", default=True
    )
    pagamento = models.ForeignKey(
        MetodoPagamento, on_delete=models.CASCADE, null=True, blank=True
    )
    custo = models.FloatField(
        verbose_name="Custo pela carona ida e volta/dia", default=0.0
    )
    deslocamentos = models.ManyToManyField(
        Deslocamento,
    )
    matricula_valida = models.BooleanField(default=True)
    endereco = models.ForeignKey(
        Endereco,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):

        self.matricula_valida = (
            True  # verificar_matricula_valida(self.comprovante, self)
        )
        print("Resultado do self.matricula_valida = ", self.matricula_valida)
        super().save(*args, **kwargs)

    def get_avaliacoes(self):

        return Avaliacao.objects.filter(
            tipo_avaliacao=AvaliacaoTipos.motorista,
            avaliado=self.id,
        )

    def get_nota_avaliacoes(self):
        avaliacoes = Avaliacao.objects.filter(
            tipo_avaliacao=AvaliacaoTipos.motorista,
            avaliado=self.id,
        )
        if len(avaliacoes) != 0:
            return sum(avaliacoes.values_list("nota", flat=True)) / len(avaliacoes)
        return 0


class Caroneiro(models.Model):
    nome = models.CharField(max_length=200)
    matricula = models.CharField(max_length=20, unique=True)
    comprovante = models.FileField(upload_to=get_upload_path)
    curso = models.CharField(max_length=200, choices=Cursos.choices)
    matricula_valida = models.BooleanField(default=True)
    endereco = models.ForeignKey(
        Endereco, on_delete=models.CASCADE, null=True, blank=True
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):

        self.matricula_valida = (
            True  # verificar_matricula_valida(self.comprovante, self)
        )
        print("Resultado do self.matricula_valida = ", self.matricula_valida)
        super().save(*args, **kwargs)

    def get_avaliacoes(self):

        return Avaliacao.objects.filter(
            tipo_avaliacao=AvaliacaoTipos.caroneiro,
            avaliado=self.id,
        )

    def get_nota_avaliacoes(self):
        avaliacoes = Avaliacao.objects.filter(
            tipo_avaliacao=AvaliacaoTipos.caroneiro,
            avaliado=self.id,
        )

        if avaliacoes:
            return sum(avaliacoes.values_list("nota", flat=True)) / len(avaliacoes)

        return 0


class Combinado(models.Model):

    caroneiro = models.ForeignKey(Caroneiro, on_delete=models.CASCADE)
    dia_semana = models.IntegerField()


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
        Caroneiro,
        verbose_name="Alunos que estão pegando carona",
        blank=True,
        null=True,
    )
    combinados = models.ManyToManyField(
        Combinado,
        verbose_name="Dias e horarios de idas conjuntas dos motoristas e caroneiros",
        blank=True,
        null=True,
    )
    ativa = models.BooleanField(default=False)

    def generate_pix(self, caroneiro):

        combinados = (
            self.combinados.all()
            .filter(
                caroneiro=caroneiro,
            )
            .count()
        )

        custo_total = (
            combinados * self.motorista.custo
            if combinados > 0 and self.motorista.custo > 0
            else 0
        )

        print("Custo do motorista; ", self.motorista.custo)
        print(
            "Custo total R$", custo_total, " para a quantia de combinados: ", combinados
        )

        return obter_qr_code_pix(
            self.motorista.nome, self.motorista.pagamento.chave, custo_total
        )

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

    def enviar_solicitacao(self, mensagem, para, de, de_tipo):

        print("criando solicitacao da carona ", self.id)

        print(mensagem)
        print(para)
        print(de)
        print(de_tipo)

        para_tipo = "caroneiro" if de_tipo == "caroneiro" else "motorista"

        solicitacao = Solicitacao.objects.create(
            mensagem=mensagem,
            carona=self,
            enviado_para=para,
            enviado_para_tipo=para_tipo,
            enviado_por=de,
            enviado_por_tipo=de_tipo,
        )


def verificar_solicitacoes(self):

    solicitacoes = (
        Solicitacao.objects.filter(
            models.Q(enviado_por=self) | models.Q(enviado_para=self),
            respondida=False,
            visualizada=False,
        )
        .distinct()
        .order_by("enviado_em")
    )

    return solicitacoes


User.add_to_class(
    "verificar_solicitacoes",
    verificar_solicitacoes,
)

User.add_to_class(
    "tipo_ativo",
    models.CharField(
        TipoUsuario.choices,
        max_length=50,
    ),
)

User.add_to_class(
    "foto",
    models.FileField(upload_to=get_upload_path, null=True),
)


class Solicitacao(models.Model):

    mensagem = models.TextField()
    carona = models.ForeignKey(Carona, on_delete=models.CASCADE)

    enviado_por = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="enviado_por"
    )
    enviado_por_tipo = models.CharField(
        choices=TipoUsuario.choices,
        max_length=100,
    )

    enviado_para = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="enviado_para"
    )
    enviado_para_tipo = models.CharField(
        choices=TipoUsuario.choices,
        max_length=100,
    )

    respondida = models.BooleanField(default=False)
    visualizada = models.BooleanField(default=False)
    aceitar = models.BooleanField(null=True, blank=True)

    enviado_em = models.DateTimeField(
        auto_now_add=True,
    )

    resposta = models.TextField(
        null=True,
        blank=True,
    )

    def aceitar_solicitacao(self, request):
        self.aceitar = True

        if self.enviado_por_tipo == "motorista":
            caroneiro = Caroneiro.objects.get(
                user_id=self.enviado_para.id,
            )

            motorista = Motorista.objects.get(
                user_id=self.enviado_por.id,
            )

            carona = Carona.objects.get(
                motorista=motorista,
            )

            if carona.vagas != 0:
                carona.caroneiros.add(
                    caroneiro,
                )
                carona.save()
            else:
                messages.error(
                    request,
                    f"A carona {self.carona.id} do motorista {self.carona.motorista.nome} está com as vagas cheias! Procure outra.",
                )
                return redirect(reverse("core:home"))
        else:
            caroneiro = Caroneiro.objects.get(
                user_id=self.enviado_por.id,
            )

            motorista = Motorista.objects.get(
                user_id=self.enviado_para.id,
            )

            carona = Carona.objects.get(
                motorista=motorista,
            )

            if carona.vagas != 0:
                carona.caroneiros.add(
                    caroneiro,
                )
                carona.save()
            else:
                messages.error(
                    request,
                    f"A carona {self.carona.id} do motorista {self.carona.motorista.nome} está com as vagas cheias! Procure outra.",
                )
                return redirect(reverse("core:home"))

        self.respondida = True
        self.visualizada = True
        self.save()

    def negar_solicitacao(self):

        self.resposta = "neguei mano se fode ai"
        self.aceitar = False
        self.save()


class MovimentacaoTipos(TextChoices):

    entrada = ("entrada", "Entrada")
    saida = ("saida", "Saida")


class Movimentacao(models.Model):

    tipo = models.CharField(
        choices=MovimentacaoTipos.choices,
        max_length=50,
    )

    valor_transacao = models.FloatField(
        default=0,
    )

    de = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Pagante")
    para = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Recebedor")
    data_movimentacao = models.DateTimeField(
        auto_now_add=True,
    )


class Extrato(models.Model):

    movimentacao = models.ManyToManyField(
        Movimentacao,
    )

    saldo = models.FloatField(
        default=0,
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def atualizar_saldo(self):

        movimentacoes = self.movimentacao.all()
        saldo = 0
        for movimentacao in movimentacoes:
            if movimentacao.tipo == "entrada":
                saldo += movimentacao.valor_transacao
            else:
                saldo -= movimentacao.valor_transacao

        self.saldo = saldo
        self.save()

    def get_entradas_mes(self):
        hoje = datetime.datetime.today()
        mes_atual = hoje.month
        ano_atual = hoje.year

        entradas_mes = (
            self.movimentacao.filter(
                tipo="entrada",
                data_movimentacao__month=mes_atual,
                data_movimentacao__year=ano_atual,
            ).aggregate(total_entradas=models.Sum("valor_transacao"))["total_entradas"]
            or 0
        )

        return entradas_mes

    def get_saidas_mes(self):
        hoje = datetime.datetime.today()
        mes_atual = hoje.month
        ano_atual = hoje.year

        saidas_mes = (
            self.movimentacao.filter(
                tipo="saida",
                data_movimentacao__month=mes_atual,
                data_movimentacao__year=ano_atual,
            ).aggregate(total_saidas=models.Sum("valor_transacao"))["total_saidas"]
            or 0
        )

        return saidas_mes
