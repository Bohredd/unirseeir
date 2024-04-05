from core.models import Deslocamento, Ponto


def get_dia_semana_num(dia_semana):

    dias = {
        "segunda": 0,
        "terça": 1,
        "quarta": 2,
        "quinta": 3,
        "sexta": 4,
    }
    if "-" in dia_semana:
        return dias[dia_semana.split("-")[0].lower()]

    return dias[dia_semana.split(" ")[0].lower()]


def registrar_deslocamentos(query_dict, motorista):

    dia_semana = None
    hora_ida = None
    hora_volta = None

    for chave, valor in query_dict.items():
        if "deslocamentos-" in chave:
            qual_chave = chave.split("-")[2]

            if qual_chave == "dia_semana":
                dia_semana = valor
            elif qual_chave == "hora_ida":
                hora_ida = valor
            elif qual_chave == "hora_volta":
                hora_volta = valor

            if (
                dia_semana is not None
                and hora_ida is not None
                and hora_volta is not None
            ):

                ## TODO: Arrumar pontos saida e destino
                deslocamento = Deslocamento.objects.create(
                    dia_semana=get_dia_semana_num(dia_semana),
                    hora_ida=hora_ida,
                    hora_volta=hora_volta,
                    ponto_saida=Ponto.objects.first(),
                    ponto_destino=Ponto.objects.last(),
                )

                dia_semana, hora_ida, hora_volta = (None, None, None)

                motorista.deslocamentos.add(deslocamento)

                motorista.save()
