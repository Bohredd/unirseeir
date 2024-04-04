from django import forms


class CadastroForm(forms.Form):

    nome = forms.CharField(max_length=200)
    email = forms.EmailField()
    data_nascimento = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"},
        ),
    )
    senha = forms.CharField(widget=forms.PasswordInput)

    tipo = forms.ChoiceField(
        choices=[("", "Escolha o tipo de Cadastro"), ("motorista", "Motorista"), ("caroneiro", "Caroneiro")],
        widget=forms.Select(attrs={"onchange": "mostrar_campo(this.value)"}),
    )
    motorista = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(attrs={"style": "display:none;"}),
    )
    caroneiro = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(attrs={"style": "display:none;"}),
    )
