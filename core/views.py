import base64

from django.shortcuts import render, get_object_or_404

from config.models import Conversa
from core.forms import CadastroForm
from core.models import Carona, Caroneiro, Motorista
from core.utils import generate_pdf, obter_qr_code_pix
from django.http import HttpResponse


def generate_contrato(request, tipo):

    if tipo == 0:

        carona = Carona.objects.first()
        caroneiro = Caroneiro.objects.first()

        pdf_bytes = generate_pdf(carona, caroneiro, tipo)

        response = HttpResponse(pdf_bytes, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="contrato.pdf"'
    else:
        carona = Carona.objects.first()
        motorista = Motorista.objects.first()

        pdf_bytes = generate_pdf(carona, motorista, tipo)

        response = HttpResponse(pdf_bytes, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="contrato.pdf"'
    return response


def login_view(request):
    pass


def register_view(request):

    if request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data["nome"]
            email = form.cleaned_data["email"]
            senha = form.cleaned_data["senha"]
            data_nascimento = form.cleaned_data["data_nascimento"]

            print(nome, email, senha, data_nascimento)

            return render(request, "cadastro.html")
    else:
        form = CadastroForm()

    return render(request, "cadastro.html", {"form": form})


def home_view(request):

    qr_code_img = obter_qr_code_pix("diogo antonio", "01074526007", "5")
    qr_code_base64 = base64.b64encode(qr_code_img.getvalue()).decode("utf-8")

    return render(request, "inicio.html", {"qr_code_base64": qr_code_base64})


def find_carona(request):

    carona = Carona.objects.filter(
        ativa=True,
        vagas__gt=0,
    )

    print(carona)


def find_caroneiro(request):

    caroneiros = list(
        Caroneiro.objects.filter(
            matricula_valida=True,
        )
    )

    for caroneiro in caroneiros:
        if Carona.objects.filter(
            ativa=True,
            caroneiros__nome=caroneiro.nome_remetente,
        ).exists():
            caroneiros.remove(caroneiro)

    print(caroneiros)


def bate_papo_view_list(request):

    conversa = Conversa.objects.filter(
        membros__in=[request.user],
    )

    print(conversa)


def bate_papo_view(request, conexao_id, conversa_id):
    pass


def bate_papo_grupo_view(request, carona_id):
    pass


def gerar_caminho_view(request, carona_id):
    pass
