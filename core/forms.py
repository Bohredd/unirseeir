from crispy_forms.bootstrap import PrependedText
from django import forms
from django.db.models import TextChoices
from django.forms import inlineformset_factory
from django.forms.widgets import DateTimeInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout

from core.models import Deslocamento, Endereco, Motorista


class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = "__all__"


class CadastroForm(forms.Form):

    nome = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'nome'}),
        max_length=200
    )

    email = forms.EmailField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'email'}))

    senha = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'senha'}),
    )
    senha_confirmacao = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'senha'}),)

    matricula = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'matricula'})
    )

    curso = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'curso'})
    )


    comprovante = forms.FileField(
        label='Comprovante',
        widget=forms.FileInput(attrs={'placeholder': 'comprovante'}),
        allow_empty_file=False,
        required=False,
    )

    tipo = forms.ChoiceField(
        label='',
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


class DeslocamentoForm(forms.ModelForm):
    horario_saida_ponto_saida = forms.TimeField(
        label="Horário de Saída no Ponto de Saída",
        widget=forms.TimeInput(attrs={"type": "time"}),
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
    matricula = forms.CharField(label="Matrícula")
    automovel = forms.CharField(label="Automóvel")

    carona_paga = forms.BooleanField(required=False)


class LoginForm(forms.Form):

    matricula = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Matricula'})
    )
    senha = forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}))

    tipo = forms.ChoiceField(
        label='',
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
            PrependedText('matricula','<span class="far fa-user"></span>', placeholder="Matricula")
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
