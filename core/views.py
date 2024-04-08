from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from config.models import Conversa
from core.decorator import is_tipo, user_in_carona
from core.forms import (
    CadastroForm,
    CaroneiroForm,
    MotoristaForm,
    LoginForm,
    MetodoPagamentoForm,
    SolicitacaoForm,
)
from core.models import (
    Carona,
    Caroneiro,
    Motorista,
    Temporario,
    MetodoPagamento,
    Solicitacao,
)
from core.utils import generate_pdf, get_user
from core.patcher import registrar_deslocamentos
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import check_password


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
            usuario = get_user(form.cleaned_data)

            if usuario is not None:

                user = authenticate(
                    username=usuario.username, password=form.cleaned_data["senha"]
                )

                if user:
                    login(request, user)

                    usuario.tipo_ativo = form.cleaned_data["tipo"]
                    usuario.save()
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
                    last_name=nome.split(" ")[0],
                    email=email,
                    password=senha,
                    tipo_ativo=tipo,
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
            else:
                if (
                    user.exists()
                    and user.first().tipo_ativo != tipo
                    and check_password(senha, user.first().password)
                ):
                    user = user.first()

                    user.tipo_ativo = tipo
                    user.save()

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
            return redirect("minhaConta", id=request.user.id)
    else:
        form = MetodoPagamentoForm()

    return render(request, "metodo_pagamento.html", {"form": form})


def register_type_view(request, tipo):

    if request.method == "POST":
        if tipo == "motorista":
            form = MotoristaForm(request.POST)
            if form.is_valid():

                matricula = form.cleaned_data["matricula"]
                automovel = form.cleaned_data["automovel"]
                carona_paga = form.cleaned_data["carona_paga"]

                temp = Temporario.objects.filter(
                    from_username=matricula,
                ).last()

                if temp is not None:

                    Motorista.objects.create(
                        nome=temp.nome,
                        matricula=temp.matricula,
                        comprovante=temp.comprovante,
                        curso=temp.curso,
                        user=request.user,
                        carona_paga=carona_paga,
                        automovel=automovel,
                    )

                    registrar_deslocamentos(
                        request.POST, Motorista.objects.get(user=request.user)
                    )

                    temp.delete()

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
                ).last()

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


def comercial_view(request):
    return HttpResponse("pagina inicial ficticia")


def logout_view(request):
    logout(request)
    return redirect("comercial")


@login_required
def home_view(request):
    print(request.user)
    # carona = Carona.objects.first()
    # qr_code_base64 = carona.generate_pix(Caroneiro.objects.first())
    # return render(request, "pix.html", {"qr_code_base64": qr_code_base64})

    if request.user.tipo_ativo == "motorista":
        caronas_ativas_do_usuario = Carona.objects.filter(
            motorista__user=request.user,
            ativa=True,
        )
    else:
        voce = Caroneiro.objects.filter(
            user=request.user,
        ).first()

        caronas_ativas_do_usuario = Carona.objects.filter(
            ativa=True,
            caroneiros=voce,
        )

    solicitacoes = request.user.verificar_solicitacoes()

    conversas = Conversa.objects.filter(
        membros=request.user,
    )

    return render(
        request,
        "home.html",
        {
            "conversas": conversas,
            "solicitacoes": solicitacoes,
            "caronas": caronas_ativas_do_usuario,
        },
    )

@login_required
def banco_view(request):

    return HttpResponse("saldo diogo antonio: R$ 189034.5348295 dolares de reais ")

@login_required
@user_in_carona()
def carona_view(request, carona):
    carona = Carona.objects.get(id=carona)

    return render(
        request,
        "carona.html",
        {
            "carona": carona,
        }
    )


def solicitacao_acao(request, situacao, solicitacao):
    # true = aceitar
    # false = recusar

    print(situacao, solicitacao)

    solicitacao = Solicitacao.objects.get(id=solicitacao)

    if situacao:
        print("ACEITAR SOLICITACAO")
        solicitacao.aceitar_solicitacao(request)
    else:
        print("RECUSAR SOLICITACAO")
        solicitacao.negar_solicitacao()

    return redirect(
        "home",
    )

@login_required
def minhas_caronas(request):
    return HttpResponse("minhas caronas ativas")


@login_required
def solicitacao_view(request, id):
    pass


@login_required
def conversa_view(request, id):

    print("id da conversa", id)

    return HttpResponse(f"id da conversa {id}")


@login_required
@is_tipo("caroneiro")
def find_carona(request):

    carona = Carona.objects.filter(
        ativa=True,
        vagas__gt=0,
    )

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

    return render(
        request,
        "find_caroneiro.html",
        {"caroneiros_disponiveis": caroneiros_disponiveis},
    )


@login_required
def bate_papo_view_list(request):

    conversa = Conversa.objects.filter(
        membros__in=[request.user],
    )

    # print(conversa)

    return render(
        request,
        "conversa_list.html",
        {
            "conversas": conversa,
        },
    )
    # return HttpResponse(conversa)


def gerar_caminho_view(request, carona_id):
    pass


@login_required
def minha_conta_view(request):
    print("minha conta view acessada")

    if request.user.tipo_ativo == "motorista":

        motorista = Motorista.objects.filter(
            user=request.user,
        ).first()

        return HttpResponse(f"minha conta motorista {motorista.nome}")

    else:
        caroneiro = Caroneiro.objects.filter(
            user=request.user,
        ).first()

        return HttpResponse(f"minha conta caroneiro {caroneiro.nome}")


def criar_solicitacao_popup(request, tipo, id):
    # tipo 1 = carona
    # tipo 2 = caroneiro

    carona = None
    caroneiro = None

    if request.method == "POST":

        form = SolicitacaoForm(request.POST)

        if form.is_valid():

            if tipo == 1:
                carona = get_object_or_404(Carona, pk=id)

                carona.enviar_solicitacao(
                    mensagem=form.cleaned_data["mensagem"],
                    para=carona.motorista.user,
                    de=request.user,
                    de_tipo=request.user.tipo_ativo,
                )
            else:

                caroneiro = get_object_or_404(Caroneiro, pk=id)

                carona = Carona.objects.get(
                    motorista__user_id=request.user.id,
                )

                Solicitacao.objects.create(
                    carona=carona,
                    mensagem=form.cleaned_data["mensagem"],
                    enviado_para=caroneiro.user,
                    enviado_por=request.user,
                    enviado_por_tipo=request.user.tipo_ativo,
                )

            return HttpResponse("<script>window.close();</script>")

    else:
        form = SolicitacaoForm()

        if tipo == 1:
            carona = get_object_or_404(Carona, pk=id)
        else:
            caroneiro = get_object_or_404(Caroneiro, pk=id)

    return render(
        request,
        "create_solicitacao.html",
        {"form": form, "carona": carona, "caroneiro_objeto": caroneiro},
    )


def BASEEDIT(request):

    return render(request, "header.html")


def switch_account_view(request):

    if request.user.tipo_ativo == "motorista":
        caroneiro = Caroneiro.objects.filter(
            user=request.user,
        )

        if caroneiro.exists():
            request.user.tipo_ativo = "caroneiro"
            request.user.save()
            messages.success(request, "Agora você está conectado como: Caroneiro!")
            return redirect(
                "home",
            )
        else:
            messages.error(
                request,
                "Não foi possível trocar o tipo de conta, garanta que você possui a conta inversa",
            )
            return redirect(
                "home",
            )
    else:
        motorista = Motorista.objects.filter(
            user=request.user,
        )

        if motorista.exists():
            request.user.tipo_ativo = "motorista"
            request.user.save()
            messages.success(request, "Agora você está conectado como: Motorista!")
            return redirect(
                "home",
            )
        else:
            messages.error(
                request,
                "Não foi possível trocar o tipo de conta, garanta que você possui a conta inversa",
            )
            return redirect(
                "home",
            )
