from django import forms
from django.forms import formset_factory

class CadastroForm(forms.Form):

    nome = forms.CharField(max_length=200)

    email = forms.EmailField()

    data_nascimento = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"},
        ),
    )

    senha = forms.CharField(widget=forms.PasswordInput)

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
    matricula = forms.CharField(label='Matrícula')
    automovel = forms.CharField(label='Automóvel')

    deslocamentos = DeslocamentoFormSet()