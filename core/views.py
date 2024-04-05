from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from config.models import Conversa
from core.forms import CadastroForm, CaroneiroForm, MotoristaForm
from core.models import Carona, Caroneiro, Motorista, Temporario
from core.utils import generate_pdf
from core.patcher import registrar_deslocamentos
from django.http import HttpResponse
from django.contrib.auth.models import User


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
            matricula = form.cleaned_data["matricula"]
            curso = form.cleaned_data["curso"]
            tipo = form.cleaned_data["tipo"]

            user = User.objects.filter(email=email, username=matricula)

            if not user.exists():

                user = User.objects.create_user(
                    username=matricula,
                    first_name=nome,
                    email=email,
                    password=senha,
                )

                user = authenticate(
                    request, username=user.username, password=user.password
                )

                comprovante = request.FILES["comprovante"]

                Temporario.objects.create(
                    comprovante=comprovante,
                    nome=nome,
                    matricula=matricula,
                    curso=curso,
                    from_username=matricula,
                )

                login(request, user)

            return redirect(register_type_view, tipo)
    else:
        form = CadastroForm()

    return render(request, "cadastro.html", {"form": form})


def register_type_view(request, tipo):

    if request.method == "POST":
        if tipo == "motorista":
            form = MotoristaForm(request.POST)
            if form.is_valid():

                registrar_deslocamentos(
                    request.POST, Motorista.objects.get(user=request.user)
                )

        elif tipo == "caroneiro":
            form = CaroneiroForm(request.POST)

            if form.is_valid():

                matricula = form.cleaned_data["matricula"]

                temp = Temporario.objects.filter(
                    matricula=matricula,
                ).first()

                Caroneiro.objects.create(
                    nome=temp.nome,
                    matricula=temp.matricula,
                    comprovante=temp.comprovante,
                    curso=temp.curso,
                    user=request.user,
                )

                temp.delete()

                return render(request, "cadastro_caroneiro.html")
        else:
            pass
    else:
        if tipo == "motorista":
            form = MotoristaForm()
        else:
            form = CaroneiroForm()

    return render(request, f"cadastro_{tipo}.html", {"form": form})


def home_view(request):

    carona = Carona.objects.first()
    qr_code_base64 = carona.generate_pix(Caroneiro.objects.first())
    return render(request, "inicio.html", {"qr_code_base64": qr_code_base64})


def find_carona(request):

    carona = Carona.objects.filter(
        ativa=True,
        vagas__gt=0,
    )

    print(carona)

    return HttpResponse(carona)


def find_caroneiro(request):

    caroneiros = list(
        Caroneiro.objects.filter(
            matricula_valida=True,
        )
    )

    caroneiros_disponiveis = []

    for caroneiro in caroneiros:
        if not Carona.objects.filter(
            ativa=True,
            caroneiros__id=caroneiro.id,
        ).exists():
            caroneiros_disponiveis.append(caroneiro)

    print(caroneiros_disponiveis)

    return HttpResponse(caroneiros_disponiveis)


def bate_papo_view_list(request):

    conversa = Conversa.objects.filter(
        membros__in=[request.user],
    )

    print(conversa)

    return HttpResponse(conversa)


def bate_papo_view(request, conexao_id, conversa_id):
    pass


def bate_papo_grupo_view(request, carona_id):
    pass


def gerar_caminho_view(request, carona_id):
    pass
