from django import forms
from django.db.models import TextChoices
from django.forms import formset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from core.models import Deslocamento, Endereco, EstadoChoices


class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = '__all__'

class CadastroForm(forms.Form):

    nome = forms.CharField(max_length=200)

    email = forms.EmailField()

    senha = forms.CharField(widget=forms.PasswordInput)
    senha_confirmacao = forms.CharField(widget=forms.PasswordInput)

    matricula = forms.CharField()

    curso = forms.CharField()

    comprovante = forms.FileField(
        allow_empty_file=False,
        required=False,
    )

    tipo = forms.ChoiceField(
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

    matricula = forms.CharField()


class DiasSemana(TextChoices):

    segunda = ("segunda", "Segunda")
    terca = ("terça", "Terça")
    quarta = ("quarta", "Quarta")
    quinta = ("quinta", "Quinta")
    sexta = ("sexta", "Sexta")


class DeslocamentoForm(forms.ModelForm): # TODO: AJUSTAR ERSSE FORM LEVANDO EM CONTA O ENDEREÇO DE DESTINO / CEP BLA BLA BLA BLA
    class Meta:
        model = Deslocamento
        fields = (
            "dia_semana",
            "horario_saida_ponto_saida",
            "ponto_saida",
            "ponto_destino",
        )


class MotoristaForm(forms.Form):
    matricula = forms.CharField(label="Matrícula")
    automovel = forms.CharField(label="Automóvel")

    carona_paga = forms.BooleanField(required=False)


class LoginForm(forms.Form):

    matricula = forms.CharField()
    senha = forms.CharField(widget=forms.PasswordInput)

    tipo = forms.ChoiceField(
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


class EditMotoristaForm(forms.Form):

    nome = forms.CharField(max_length=200)
    email = forms.EmailField()

    senha = forms.CharField(widget=forms.PasswordInput)
    senha_confirmacao = forms.CharField(widget=forms.PasswordInput)

    matricula = forms.CharField()

    automovel = forms.CharField()
    carona_paga = forms.BooleanField()


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
