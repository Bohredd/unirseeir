from crispy_forms.bootstrap import PrependedText
from django import forms
from django.db.models import TextChoices, Q
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from django.forms.models import ModelChoiceIterator
from core.models import (
    Deslocamento,
    Endereco,
    Cursos,
    Carona,
    Motorista,
    Caroneiro,
    EstadoChoices,
)


class EnderecoForm(forms.ModelForm):
    cep = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": "CEP", "id": "id_cep"})
    )
    cidade = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Cidade", "id": "id_cidade"}),
    )
    logradouro = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Logradouro", "id": "id_logradouro"}
        ),
    )
    bairro = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Bairro", "id": "id_bairro"}),
    )
    numero = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Numero", "id": "id_numero"}),
    )
    complemento = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Complemento", "id": "id_complemento"}
        ),
    )

    class Meta:
        model = Endereco
        fields = [
            "cep",
            "estado",
            "cidade",
            "logradouro",
            "bairro",
            "numero",
            "complemento",
        ]

    class Media:
        js = ("endereco_form.js",)


class CadastroForm(forms.Form):
    nome = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Digite seu nome"}),
        max_length=200,
    )

    email = forms.EmailField(
        initial="seu@email.aqui",
        label="",
        widget=forms.TextInput(attrs={"placeholder": "email"}),
    )

    senha = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={"placeholder": "Digite sua senha"}),
    )
    senha_confirmacao = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={"placeholder": "Digite sua senha"}),
    )

    matricula = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": "Digite sua matricula"})
    )

    curso = forms.ChoiceField(
        choices=Cursos.choices,
        label="",
        widget=forms.Select(),
    )

    comprovante = forms.FileField(
        label="Comprovante",
        widget=forms.FileInput(
            attrs={"placeholder": "Selecione seu comprovante de Matrícula"}
        ),
        allow_empty_file=False,
        required=False,
    )

    tipo = forms.ChoiceField(
        label="",
        choices=[
            ("", "Escolha o tipo de Cadastro"),
            ("motorista", "Motorista"),
            ("caroneiro", "Caroneiro"),
        ],
        widget=forms.Select(),
    )

    endereco = EnderecoForm()

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        senha_confirmacao = cleaned_data.get("senha_confirmacao")

        if senha and senha_confirmacao and senha != senha_confirmacao:
            raise forms.ValidationError("As senhas não coincidem.")


class CaroneiroForm(forms.Form):
    matricula = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Digite sua matricula"}), label=""
    )


class DiasSemana(TextChoices):
    segunda = ("segunda", "Segunda")
    terca = ("terça", "Terça")
    quarta = ("quarta", "Quarta")
    quinta = ("quinta", "Quinta")
    sexta = ("sexta", "Sexta")


class DeslocamentoForm(forms.ModelForm):
    horario_saida_ponto_saida = forms.TimeField(
        label="Horário de Saída no Ponto de Saída",
        widget=forms.TimeInput(attrs={"type": "time"}),
    )
    cep = forms.CharField(max_length=200, label="CEP do Ponto de Saída", help_text="Digite a Cidade e o Estado Junto*"
                          )

    class Meta:
        model = Deslocamento
        fields = (
            "dia_semana",
            "horario_saida_ponto_saida",
            "ponto_saida_endereco",
            "ponto_destino_endereco",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["horario_saida_ponto_saida"].widget.attrs.update(
            {"class": "form-control"}
        )


class MotoristaForm(forms.Form):
    matricula = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Digite sua matricula"}), label=""
    )
    automovel = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Automovel"}), label=""
    )

    carona_paga = forms.BooleanField(required=False)


class LoginForm(forms.Form):
    matricula = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": "Matricula"})
    )
    senha = forms.CharField(
        label="", widget=forms.PasswordInput(attrs={"placeholder": "Senha"})
    )

    tipo = forms.ChoiceField(
        label="",
        choices=[
            ("", "Tipo de Conta"),
            ("motorista", "Motorista"),
            ("caroneiro", "Caroneiro"),
        ],
        widget=forms.Select(),
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Login"))
        self.helper.layout = Layout(
            PrependedText(
                "matricula",
                '<span class="far fa-user"></span>',
                placeholder="Matricula",
            )
        )


class MetodoPagamentoForm(forms.Form):
    tipo_pagamento = forms.ChoiceField(
        choices=[
            ("", "Tipo de Pagamento"),
            ("pix", "PIX"),
        ]
    )

    chave = forms.CharField()

    custo = forms.DecimalField()


class SolicitacaoForm(forms.Form):
    mensagem = forms.CharField(label="Mensagem", widget=forms.Textarea())


class EditCaroneiroForm(forms.Form):
    nome = forms.CharField(max_length=200)
    email = forms.EmailField()

    senha = forms.CharField(widget=forms.PasswordInput)
    senha_confirmacao = forms.CharField(widget=forms.PasswordInput)

    matricula = forms.CharField()

    foto = forms.FileField(
        label="Foto de Perfil",
        widget=forms.FileInput(
            attrs={"placeholder": "Selecione a Foto para o seu Perfil"}
        ),
        allow_empty_file=False,
        required=False,
    )


class EditMotoristaForm(forms.Form):
    nome = forms.CharField(max_length=200)
    email = forms.EmailField()

    senha = forms.CharField(widget=forms.PasswordInput)
    senha_confirmacao = forms.CharField(widget=forms.PasswordInput)

    matricula = forms.CharField()

    automovel = forms.CharField()
    carona_paga = forms.BooleanField()

    foto = forms.FileField(
        label="Foto de Perfil",
        widget=forms.FileInput(
            attrs={"placeholder": "Selecione a Foto para o seu Perfil"}
        ),
        allow_empty_file=False,
        required=False,
    )


class ValidarCaronaForms(forms.ModelForm):
    class Meta:
        model = Carona
        fields = ["ativa"]


class MensagemForm(forms.Form):
    conteudo = forms.CharField(
        widget=forms.Textarea(), label="Digite sua mensagem aqui"
    )


class CaronaForm(forms.Form):
    tipo = forms.ChoiceField(
        choices=[
            ("", "Tipo de Automóvel"),
            ("carro", "Carro"),
            ("moto", "Moto"),
        ],
        widget=forms.Select(),
    )


class EsqueciSenha(forms.Form):
    matricula = forms.CharField(label="Matricula")

    email = forms.EmailField()


class FotoPerfilForm(forms.Form):
    foto = forms.FileField(
        label="Foto de Perfil",
        widget=forms.FileInput(
            attrs={"placeholder": "Selecione a Foto para o seu Perfil"}
        ),
        allow_empty_file=False,
        required=False,
    )


class CriarCombinadoForms(forms.Form):
    endereco_ponto_encontro = forms.CharField()
    horario_encontro_ponto_encontro = forms.TimeField(
        widget=forms.TimeInput(attrs={"type": "time"})
    )
    deslocamento = forms.ChoiceField(choices=[])
    estado = forms.ChoiceField(choices=EstadoChoices.choices)
    cidade = forms.CharField()

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super(CriarCombinadoForms, self).__init__(*args, **kwargs)
        if request:
            if request.user.tipo_ativo == "motorista":
                carona_obj = Carona.objects.filter(
                    motorista__user=request.user,
                    ativa=True,
                ).first()
            else:
                carona_obj = Carona.objects.filter(
                    caroneiros__user=request.user,
                    ativa=True,
                ).first()
            if carona_obj:
                deslocamentos = carona_obj.motorista.deslocamentos.values_list(
                    "id",
                    "dia_semana",
                    "horario_saida_ponto_saida",
                    "ponto_saida_endereco",
                    "ponto_destino_endereco",
                )
                formatted_deslocamentos = self.format_deslocamentos(deslocamentos)
                self.fields["deslocamento"].choices = formatted_deslocamentos

    def format_deslocamentos(self, deslocamentos):
        formatted_list = [("", "Selecione um deslocamento")]
        for deslocamento in deslocamentos:
            formatted_deslocamento = (
                deslocamento[0],
                f"{deslocamento[1].title()} - {deslocamento[2]} - {deslocamento[3]} -> {deslocamento[4]}",
            )
            formatted_list.append(formatted_deslocamento)
        return formatted_list
