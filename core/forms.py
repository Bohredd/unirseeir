from django import forms
from django.forms import formset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


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


class CaroneiroForm(forms.Form):

    matricula = forms.CharField()


class DeslocamentoForm(forms.Form):
    dia_semana = forms.CharField()
    hora_ida = forms.TimeField()
    hora_volta = forms.TimeField()


DeslocamentoFormSet = formset_factory(DeslocamentoForm, extra=1)


class MotoristaForm(forms.Form):
    matricula = forms.CharField(label="Matrícula")
    automovel = forms.CharField(label="Automóvel")

    carona_paga = forms.BooleanField()

    deslocamentos = DeslocamentoFormSet()


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
    deslocamentos = DeslocamentoFormSet()
