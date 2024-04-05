from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login
from config.models import Conversa
from core.decorator import is_tipo, is_conta_do_requester
from core.forms import (
    CadastroForm,
    CaroneiroForm,
    MotoristaForm,
    LoginForm,
    MetodoPagamentoForm,
    SolicitacaoForm,
)
from core.models import Carona, Caroneiro, Motorista, Temporario, MetodoPagamento
from core.utils import generate_pdf, get_user
from core.patcher import registrar_deslocamentos
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User


@login_required
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

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)

            usuario = get_user(form.cleaned_data)

            if usuario is not None:

                user = authenticate(
                    username=usuario.username, password=form.cleaned_data["senha"]
                )

                if user:
                    login(request, user)

                    usuario.tipo_ativo = form.cleaned_data["tipo"]
                    usuario.save()
                    print("authenticado")
                    return redirect(
                        home_view,
                    )
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


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


def metodo_pagamento_view(request):
    if request.method == "POST":
        form = MetodoPagamentoForm(request.POST)
        if form.is_valid():
            tipo_pagamento = form.cleaned_data["tipo_pagamento"]
            chave = form.cleaned_data["chave"]
            custo = form.cleaned_data["custo"]

            motorista = Motorista.objects.get(
                user=request.user,
            )

            motorista.custo = custo
            motorista.save()

            metodo_pagamento = MetodoPagamento.objects.create(
                nome=tipo_pagamento,
                chave=chave,
            )

            motorista.pagamento = metodo_pagamento
            motorista.save()

            print(tipo_pagamento, chave, custo)
            print(request.user.id)
            return redirect("minhaConta", id=request.user.id)
    else:
        form = MetodoPagamentoForm()

    return render(request, "metodo_pagamento.html", {"form": form})


def register_type_view(request, tipo):

    if request.method == "POST":
        if tipo == "motorista":
            form = MotoristaForm(request.POST)
            if form.is_valid():

                registrar_deslocamentos(
                    request.POST, Motorista.objects.get(user=request.user)
                )

                matricula = form.cleaned_data["matricula"]
                automovel = form.cleaned_data["automovel"]
                carona_paga = form.cleaned_data["carona_paga"]

                temp = Temporario.objects.filter(
                    from_username=matricula,
                ).last()

                if temp is not None:

                    motorista = Motorista.objects.create(
                        nome=temp.nome,
                        matricula=temp.matricula,
                        comprovante=temp.comprovante,
                        curso=temp.curso,
                        user=request.user,
                        carona_paga=carona_paga,
                        automovel=automovel,
                    )

                    if carona_paga:
                        return redirect(
                            "metodoPagamento",
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


@login_required
def home_view(request):

    carona = Carona.objects.first()
    qr_code_base64 = carona.generate_pix(Caroneiro.objects.first())
    return render(request, "pix.html", {"qr_code_base64": qr_code_base64})


@login_required
@is_tipo("caroneiro")
def find_carona(request):

    carona = Carona.objects.filter(
        ativa=True,
        vagas__gt=0,
    )

    print(carona)

    return render(request, "find_carona.html", {"caronas": carona})


@login_required
@is_tipo("motorista")
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


@login_required
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


@login_required
@is_conta_do_requester()
def minha_conta_view(request, id):
    print("minha conta view acessada")

    return HttpResponse("minha conta")


def criar_solicitacao_popup(request, id):

    carona = get_object_or_404(Carona, pk=id)

    if request.method == "POST":

        form = SolicitacaoForm(request.POST)

        if form.is_valid():

            print(form.cleaned_data)

            carona.enviar_solicitacao(
                mensagem=form.cleaned_data['mensagem'],
                para=carona.motorista.user,
                de=request.user,
                de_tipo=request.user.tipo_ativo,
            )

            return HttpResponse("<script>window.close();</script>")
    else:
        form = SolicitacaoForm()

    return render(request, "create_solicitacao.html", {"form": form, "carona": carona})
