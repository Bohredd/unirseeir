from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from config.models import Conversa, Mensagem, Conexao
from core.decorator import is_tipo, user_in_carona
from core.forms import (
    CadastroForm,
    CaroneiroForm,
    MotoristaForm,
    LoginForm,
    MetodoPagamentoForm,
    SolicitacaoForm,
    EditMotoristaForm,
    EditCaroneiroForm,
    MensagemForm,
    DeslocamentoForm,
    CaronaForm,
    EnderecoForm,
    EsqueciSenha,
)
from core.models import (
    Carona,
    Caroneiro,
    Motorista,
    Temporario,
    MetodoPagamento,
    Solicitacao,
    Extrato,
    Deslocamento,
    Endereco,
)
from core.utils import (
    generate_pdf,
    get_user,
    get_menor_distancia_deslocamentos,
    get_menor_distancia_cep,
    gerar_senha,
)
from django.db import models
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
            senha_confirmacao = form.cleaned_data["senha_confirmacao"]
            matricula = form.cleaned_data["matricula"]
            curso = form.cleaned_data["curso"]
            tipo = form.cleaned_data["tipo"]
            print(request.POST)
            endereco_form = form.endereco
            # cep = form.cleaned_data["cep"]
            # estado = form.cleaned_data["estado"]
            # cidade = form.cleaned_data["cidade"]
            # logradouro = form.cleaned_data["logradouro"]
            # bairro = form.cleaned_data["bairro"]
            # numero = form.cleaned_data["numero"]
            # complemento = form.cleaned_data["complemento"]

            user = User.objects.filter(email=email, username=matricula)

            ##print(endereco)

            if not user.exists() and senha == senha_confirmacao:

                user = User.objects.create_user(
                    username=matricula,
                    first_name=nome,
                    last_name=nome.split(" ")[0],
                    email=email,
                    password=senha,
                    tipo_ativo=tipo,
                )

                user.save()

                Endereco.objects.create(
                    cep=endereco_form.cep,
                    cidade=endereco_form.cidade,
                    estado=endereco_form.estado,
                    logradouro=endereco_form.logradouro,
                    bairro=endereco_form.bairro,
                    numero=endereco_form.numero,
                    complemento=endereco_form.complemento,
                    usuario=user,
                )
                endereco = endereco_form.save(commit=False)
                endereco.save()

                Extrato.objects.create(
                    usuario=user,
                )

                if "comprovante" in request.FILES:
                    comprovante = request.FILES["comprovante"]
                else:
                    comprovante = None

                Temporario.objects.create(
                    comprovante=comprovante,
                    nome=nome,
                    matricula=matricula,
                    curso=curso,
                    from_username=matricula,
                )

                user = authenticate(request, username=matricula, password=senha)

                login(request, user)
            else:
                if (
                    user.exists()
                    and user.first().tipo_ativo != tipo
                    and check_password(senha, user.first().password)
                    and senha == senha_confirmacao
                ):
                    user = user.first()

                    user.tipo_ativo = tipo
                    user.save()

                    Extrato.objects.create(
                        usuario=user,
                    )

                    user = authenticate(request, username=matricula, password=senha)

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
        form_cadastro = CadastroForm()
        form_endereco = EnderecoForm()

    return render(
        request,
        "cadastro.html",
        {"form_cadastro": form_cadastro, "form_endereco": form_endereco},
    )


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
            return redirect("minhaConta")
    else:
        form = MetodoPagamentoForm()

    return render(request, "metodo_pagamento.html", {"form": form})


def register_type_view(request, tipo):

    if request.method == "POST":
        if tipo == "motorista":
            form = MotoristaForm(request.POST)
            if form.is_valid():

                print("form valido", form.cleaned_data)

                matricula = form.cleaned_data["matricula"]
                automovel = form.cleaned_data["automovel"]
                carona_paga = form.cleaned_data["carona_paga"]

                temp = Temporario.objects.filter(
                    from_username=matricula,
                ).last()

                if temp is not None:

                    usuario = User.objects.get(username=matricula)

                    Motorista.objects.create(
                        nome=temp.nome,
                        matricula=temp.matricula,
                        comprovante=temp.comprovante,
                        curso=temp.curso,
                        user=usuario,
                        carona_paga=carona_paga,
                        automovel=automovel,
                    )

                    # registrar_deslocamentos(
                    #    request.POST, Motorista.objects.get(user=request.user)
                    # )

                    temp.delete()

                    if carona_paga:
                        print("carona paga true")
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
                ).save()

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
    carona = Carona.objects.first()
    qr_code_base64 = carona.generate_pix(Caroneiro.objects.first())
    return render(request, "pix.html", {"qr_code_base64": qr_code_base64})


def logout_view(request):
    logout(request)
    return redirect("comercial")


@login_required
def home_view(request):
    print(request.user)

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

    extrato = Extrato.objects.filter(
        usuario=request.user,
    ).first()
    if extrato:
        extrato.atualizar_saldo()

        movimentacoes = extrato.movimentacao.all().order_by("-data_movimentacao")[:10]

        print(movimentacoes)
        return render(
            request,
            "banco.html",
            {
                "extrato": extrato,
                "movimentacoes": movimentacoes,
            },
        )

    messages.error(
        request,
        "Você não tem um extrato! Enviamos uma notificação aos desenvolvedores para que criem",
    )
    return redirect("home")


@login_required
@is_tipo("motorista")
def criar_minha_carona(request):

    if Carona.objects.filter(
        motorista__user=request.user,
    ).exists():
        messages.warning(
            request,
            "Você já é motorista de uma carona!",
        )
        return redirect(
            "home",
        )

    if request.method == "POST":

        form = CaronaForm(request.POST)

        if form.is_valid():
            tipo = form.cleaned_data["tipo"]

            print(tipo)

            carona = Carona.objects.create(
                tipo=tipo,
                motorista=Motorista.objects.get(user=request.user),
            )

            return redirect("caronaView", carona.id)

    else:
        form = CaronaForm()

    return render(
        request,
        "create_carona.html",
        {
            "request": request,
            "form": form,
        },
    )


@login_required
@is_tipo("caroneiro")
def ver_deslocamentos_motoristas(request, carona):

    carona = Carona.objects.get(id=carona)

    print(carona)

    return render(
        request,
        "ver_deslocamentos.html",
        {
            "carona": carona,
        },
    )


@login_required
@user_in_carona()
def carona_view(request, carona):
    carona = Carona.objects.get(id=carona)

    return render(
        request,
        "carona.html",
        {
            "carona": carona,
        },
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

    if request.user.tipo_ativo == "motorista":
        caronas_ativas_do_usuario = Carona.objects.filter(
            motorista__user=request.user,
        )
    else:
        voce = Caroneiro.objects.filter(
            user=request.user,
        ).first()

        caronas_ativas_do_usuario = Carona.objects.filter(
            ativa=True,
            caroneiros=voce,
        )

    caronas_disponiveis = Carona.objects.filter(
        ativa=True,
        vagas__gt=0,
    )

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
        "minhas_caronas.html",
        {
            "request": request,
            "caronas": caronas_ativas_do_usuario,
            "caronas_disponiveis": caronas_disponiveis,
            "caroneiros_disponiveis": caroneiros_disponiveis,
        },
    )


@login_required
def solicitacao_view(request, id):

    solicitacao = Solicitacao.objects.get(pk=id)

    return render(
        request,
        "ver_solicitacao.html",
        {"solicitacao": solicitacao},
    )


@login_required
def conversa_view(request, id):

    if request.method == "POST":
        form = MensagemForm(request.POST)

        if form.is_valid():
            conteudo = form.cleaned_data["conteudo"]

            mensagem = Mensagem.objects.create(
                enviado_por=request.user,
                conteudo=conteudo,
            )

            conexao, _ = Conexao.objects.get_or_create(
                usuario=request.user,
            )

            conexao.ativa = True
            conexao.save()

            mensagem.send_message(
                conexao,
            )

            conexao.ativa = False
            conexao.save()

            return redirect(
                "conversa",
                id=id,
            )

    else:

        form = MensagemForm()

    conversa = Conversa.objects.get(
        pk=id,
    )

    mensagens = conversa.mensagens.all()

    mensagens.update(
        visualizado=True,
    )

    mensagens = mensagens[:10]

    print(mensagens)

    return render(
        request,
        "conversa_view.html",
        {
            "conversa": conversa,
            "mensagens": mensagens,
            "request": request,
            "form": form,
        },
    )


@login_required
@is_tipo("caroneiro")
def find_carona(request):

    latitude, longitude = (None, None)
    if request.method == "GET":

        latitude = request.GET.get("la")
        longitude = request.GET.get("lo")

        print(latitude, longitude)

    carona = Carona.objects.filter(
        ativa=True,
        vagas__gt=0,
    )

    if latitude and longitude:
        caronas_ordenadas = []

        for carona_obj in carona.all():
            menor_distancia = get_menor_distancia_deslocamentos(
                latitude, longitude, carona_obj
            )
            caronas_ordenadas.append((carona_obj, menor_distancia))

        caronas_ordenadas.sort(key=lambda x: x[1], reverse=True)

        carona = [carona_obj for carona_obj, _ in caronas_ordenadas]

    print(carona)
    return render(
        request,
        "find_carona.html",
        {"caronas": carona, "latitude": latitude, "longitude": longitude},
    )


@login_required
@is_tipo("motorista")
def find_caroneiro(request):

    latitude, longitude = (None, None)

    if request.method == "GET":
        latitude = request.GET.get("la")
        longitude = request.GET.get("lo")

    print(latitude, longitude)

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

    if latitude is not None and longitude is not None:
        caroneiros_disponiveis.sort(
            key=lambda c: get_menor_distancia_cep(latitude, longitude, c.endereco.cep)
        )

    return render(
        request,
        "find_caroneiro.html",
        {
            "caroneiros_disponiveis": caroneiros_disponiveis,
            "latitude": latitude,
            "longitude": longitude,
        },
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


def gerar_caminho_view(request, carona):

    carona = Carona.objects.get(id=carona)
    print(carona)
    return render(
        request,
        "generate_caminho.html",
        {
            "carona": carona,
        },
    )


@login_required
def minha_conta_view(request):

    if request.user.tipo_ativo == "motorista":

        if request.method == "POST":

            dados = request.POST
            print(dados)

        objeto = Motorista.objects.filter(
            user=request.user,
        ).first()

        print(objeto)

        form = EditMotoristaForm(
            initial={
                "nome": objeto.nome,
                "email": request.user.email,
                "senha": "*" * len(request.user.password),
                "senha_confirmacao": "*" * len(request.user.password),
                "matricula": objeto.matricula,
                "automovel": objeto.automovel,
                "carona_paga": objeto.carona_paga,
            }
        )
    else:

        if request.method == "POST":

            dados = request.POST
            print(dados)

        objeto = Caroneiro.objects.filter(
            user=request.user,
        ).first()

        print(objeto)

        form = EditCaroneiroForm(
            initial={
                "nome": objeto.nome,
                "email": request.user.email,
                "senha": "*" * len(request.user.password),
                "senha_confirmacao": "*" * len(request.user.password),
                "matricula": objeto.matricula,
            }
        )

    return render(
        request,
        "minha_conta.html",
        {"form": form},
    )


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


@is_tipo("motorista")
@login_required
def meus_deslocamentos_view(request):
    motorista = Motorista.objects.get(user=request.user)
    DeslocamentoFormSet = modelformset_factory(
        Deslocamento, form=DeslocamentoForm, extra=1
    )

    if request.method == "POST":
        formset = DeslocamentoFormSet(
            request.POST, queryset=motorista.deslocamentos.all()
        )
        if formset.is_valid():
            instances = formset.save()

            for instance in instances:
                motorista.deslocamentos.add(
                    instance,
                )

            motorista.save()

            messages.success(request, "Deslocamentos salvos com sucesso!")
            return redirect("home")
    else:
        formset = DeslocamentoFormSet(queryset=motorista.deslocamentos.all())

    return render(request, "meus_deslocamentos.html", {"formset": formset})


def solicitacao_list(request):

    solicitacoes = solicitacoes = (
        Solicitacao.objects.filter(
            models.Q(enviado_por=request.user) | models.Q(enviado_para=request.user),
            respondida=False,
            visualizada=False,
        )
        .distinct()
        .order_by("enviado_em")
    )

    return render(
        request,
        "solicitacao_list.html",
        {"solicitacoes": solicitacoes},
    )


def landing_view(request):
    return render(request, "home2.html")


def esqueci_minha_senha(request):

    if request.method == "POST":

        form = EsqueciSenha(request.POST)

        if form.is_valid():
            matricula = form.cleaned_data["matricula"]
            email = form.cleaned_data["email"]

            print(matricula, email)

            user = User.objects.filter(
                email=email,
                username=matricula,
            )

            if user.exists():

                nova_senha = gerar_senha()
                user_obj = user.first()

                # Alterar a senha do usuário
                user_obj.set_password(nova_senha)
                user_obj.save()


                assunto = "Redefinição de Senha"
                mensagem = f"""
                Ei, {user_obj.first_name}!

                Sua nova senha chegou!

                Nova senha: {nova_senha}

                Copie a senha acima e use-a para acessar sua conta.

                Atenciosamente,
                UNIr-se e Ir.
                """
                rementente = "unirseeir@gmail.com"
                destinatario = [
                    f"{user_obj.email}",
                ]
                send_mail(
                    assunto,
                    mensagem,
                    rementente,
                    destinatario,
                )

                messages.success(
                    request,
                    f"Senha alterada com sucesso! Verifique seu E-Mail!",
                )

                return redirect(
                    "login",
                )

            else:
                messages.error(
                    request,
                    "Não há nenhum usuário com essa Matrícula e/ou E-Mail!",
                )

                return redirect("esqueciMinhaSenha")

    else:
        form = EsqueciSenha()

    return render(
        request,
        "esqueci_senha.html",
        {"form": form},
    )
