from django import template
from django.db.models import Q

register = template.Library()


@register.simple_tag
def conversa_get_mensagem_membro(request, conversa):

    usuarios = list(conversa.get_membros())

    if request.user.first_name in usuarios:
        usuarios.remove(request.user.first_name)

        if len(usuarios) == 1:
            return usuarios[0]
        else:
            usuarios.append("e Você")
            string_arrumada = ""

            for index, usuario in enumerate(usuarios):

                if index == len(usuarios) - 2:
                    string_arrumada += f"{usuario} "
                elif index != len(usuarios) - 1:
                    string_arrumada += f"{usuario}, "
                else:
                    string_arrumada += f"{usuario}."

            return string_arrumada


@register.simple_tag
def conversa_get_mensagens_nao_visualizadas(request, conversa):

    mensagens = conversa.mensagens.all().filter(
        visualizado=False,
    )

    mensagens = mensagens.filter(~Q(enviado_por=request.user))

    return len(mensagens)


@register.simple_tag
def get_ultimo_enviador_mensagem_e_menssagem(conversa):

    mensagem = conversa.mensagens.all().last()

    return f"{mensagem.enviado_por.first_name}: {mensagem.conteudo}"


@register.simple_tag
def get_carona_membros(carona):

    membros = carona.caroneiros.all().values_list("nome", flat=True)

    if len(membros) == 1:
        return membros[0]
    else:
        if len(membros) > 1:
            string_arrumada = ""

            for index, usuario in enumerate(membros):

                if index == len(membros) - 2:
                    string_arrumada += f"{usuario} "
                elif index != len(membros) - 1:
                    string_arrumada += f"{usuario}, "
                else:
                    string_arrumada += f"{usuario}."

            return string_arrumada

    return 0

@register.simple_tag
def get_carona_motorista(request, carona):

    print(request.user.first_name)
    print(carona.motorista.nome)

    if carona.motorista.nome == request.user.first_name:
        return "Você"

    return carona.motorista.nome
