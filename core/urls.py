from django.urls import path
from core.views import (
    generate_contrato,
    find_carona,
    find_caroneiro,
    bate_papo_view_list,
    carona_view,
    solicitacao_view,
    conversa_view,
    gerar_caminho_view,
    home_view,
    login_view,
    logout_view,
    register_view,
    register_type_view,
    minha_conta_view,
    metodo_pagamento_view,
    criar_solicitacao_popup,
    BASEEDIT,
    comercial_view,
    switch_account_view,
    minhas_caronas,
    solicitacao_acao,
    banco_view,
    meus_deslocamentos_view,
    ver_deslocamentos_motoristas,
    criar_minha_carona,
    solicitacao_list,
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
    path("carona/gerar/caminho/<int:carona>/", gerar_caminho_view, name="gerarCaminho"),
    path("account/", minha_conta_view, name="minhaConta"),
    path("cadastro/pagamento/", metodo_pagamento_view, name="metodoPagamento"),
    path(
        "solicitacao/criar/<int:tipo>/<int:id>/",
        criar_solicitacao_popup,
        name="criarSolicitacao",
    ),
    path("BASEEDIT", BASEEDIT, name="BASEEDIT"),
    path("logout/", logout_view, name="logout"),
    path("inicio/", comercial_view, name="comercial"),
    path("conversa/ver/<int:id>/", conversa_view, name="conversa"),
    path("switch/account/", switch_account_view, name="switchAccount"),
    path("carona/ver/<int:carona>/", carona_view, name="caronaView"),
    path("carona/ver/minhas/", minhas_caronas, name="minhasCaronas"),
    path(
        "solicitacao/ver/<int:solicitacao>/", solicitacao_view, name="solicitacaoView"
    ),
    path(
        "solicitacao/<int:situacao>/<int:solicitacao>/",
        solicitacao_acao,
        name="solicitacaoAcao",
    ),
    path("solicitacao/list/", solicitacao_list, name="solicitacaoList"),
    path("banco/", banco_view, name="bancoView"),
    path("deslocamentos/meus/", meus_deslocamentos_view, name="meusDeslocamentos"),
    path(
        "carona/ver/deslocamentos/<int:carona>/",
        ver_deslocamentos_motoristas,
        name="verDeslocamentosMotorista",
    ),
    path("carona/criar/", criar_minha_carona, name="criarMinhaCarona"),
]
