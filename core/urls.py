"""
URL configuration for unirseir project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
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
        "conversa/dm/<int:conexao_id>/<int:conversa_id>",
        bate_papo_view,
        name="conversaDM",
    ),
    path("conversa/group/<int:carona_id>/", bate_papo_grupo_view, name="batePapoGroup"),
    path(
        "carona/gerar_caminho/<int:carona_id>", gerar_caminho_view, name="gerarCaminho"
    ),
]
