from django.urls import path
from core.views import (
    generate_contrato,
    find_carona,
    find_caroneiro,
    bate_papo_view_list,
    bate_papo_view,
    bate_papo_grupo_view,
    gerar_caminho_view,
    home_view,
    login_view,
    register_view,
    register_type_view,
    minha_conta_view,
    metodo_pagamento_view,
    criar_solicitacao_popup,
)

urlpatterns = [
    path("", home_view, name="home"),
    path("acessar/", login_view, name="login"),
    path("cadastro/", register_view, name="register"),
    path("cadastro/<str:tipo>", register_type_view, name="registerType"),
    path("gerar/<int:tipo>", generate_contrato, name="gerarContrato"),
    path("find/carona/", find_carona, name="findCarona"),
    path("find/caroneiro/", find_caroneiro, name="findCaroneiro"),
    path("conversa/list/", bate_papo_view_list, name="conversaList"),
    path(
        "conversa/dm/<int:conexao>/<int:conversa>",
        bate_papo_view,
        name="conversaDM",
    ),
    path("conversa/group/<int:carona>/", bate_papo_grupo_view, name="batePapoGroup"),
    path("carona/gerar_caminho/<int:carona>/", gerar_caminho_view, name="gerarCaminho"),
    path("account/<int:id>/", minha_conta_view, name="minhaConta"),
    path("cadastro/pagamento/", metodo_pagamento_view, name="metodoPagamento"),
    path("solicitacao/criar/<int:id>/", criar_solicitacao_popup, name="criarSolicitacao"),
]
