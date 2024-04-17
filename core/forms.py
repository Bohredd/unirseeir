from crispy_forms.bootstrap import PrependedText
from django import forms
from django.db.models import TextChoices
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout

from core.models import Deslocamento, Endereco, Cursos, Carona


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
        fields = ['ativa']

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
