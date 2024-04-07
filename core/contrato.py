import datetime
import locale

from jinja2 import Template


def get_template_contrato(carona, objeto, tipo):

    horario = datetime.datetime.now() + datetime.timedelta(hours=-3)
    horario = horario.time().strftime("%H:%M")

    rendered_template = None

    if tipo == 1:
        template_contrato = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title> Contrato UNIr-se e Ir</title>
        
            <style>
                .logo-superior {
                    width: 200px;
                    height: 200px;
                    margin-top: 10px;
                }
        
                .logo-inferior {
                    width: 200px;
                    height: 200px;
                    margin-top: auto;
                    margin-bottom: 10px;
                }
        
                h1 {
                    color: white;
                    font-size: 35px;
                }
        
                h2 {
                    margin: 0;
                    font-size: 15px;
                    color: #FF914D;
                }
            </style>
        </head>
        <body>
            <img src="" class="logo-superior">
            <h1>Contrato Blockchain de Carona</h1>
            <h2>UNIr-se e Ir</h2>
            <p class="dados-contrato">
                Eu, {{ caroneiro.nome }}, da matrícula {{ caroneiro.matricula }} do curso {{ caroneiro.curso }}, assumo que irei ter respeito com os colegas que estarei
                oferecendo a carona. <br>
                Assumo também que irei prezar pela pontualidade marcada com {{ caroneiros }}<br>
            </p>
        
            <div id="dados">
                <p> {{ hoje_str }}, Santa Maria, Rio Grande do Sul, Brasil. {{ horario_hoje }} </p>
            </div>
        
            <hr style="margin-top: 150px;color: #ffffff; width: 50px">
            <div id="ceo">
                <p> Diogo Antonio</p>
                <p> CEO & Desenvolvedor BackEnd</p>
            </div>
        
            <img src="" class="logo-inferior">
        </body>
        </html>
        """

        template = Template(template_contrato)

        locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

        hoje = datetime.datetime.now().date().strftime("%d de %B de %Y")

        rendered_template = template.render(
            caroneiros=carona.get_caroneiros_nomes(template=True),
            caroneiro=objeto,
            hoje_str=hoje,
            horario_hoje=horario,
        )
    else:
        template_contrato = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title> Contrato UNIr-se e Ir</title>
        
            <style>
                .logo-superior {
                    width: 200px;
                    height: 200px;
                    margin-top: 10px;
                }
        
                .logo-inferior {
                    width: 200px;
                    height: 200px;
                    margin-top: auto;
                    margin-bottom: 10px;
                }
        
                h1 {
                    color: white;
                    font-size: 35px;
                }
        
                h2 {
                    margin: 0;
                    font-size: 15px;
                    color: #FF914D;
                }
            </style>
        </head>
        <body>
            <img src="" class="logo-superior">
            <h1>Contrato Blockchain de Carona</h1>
            <h2>UNIr-se e Ir</h2>
            <p class="dados-contrato">
                Eu, {{ caroneiro.nome }}, da matrícula {{ caroneiro.matricula }} do curso {{ caroneiro.curso }}, assumo que irei ter respeito com os colegas que também
                estarão utilizando da carona. <br>
                Assumo também que irei prezar pelo cuidado com o automóvel {{ carona.motorista.automovel }} do motorista {{ carona.motorista.nome }} de matrícula {{ carona.motorista.matricula }}.<br>
            </p>
        
            <div id="dados">
                <p> {{ hoje_str }}, Santa Maria, Rio Grande do Sul, Brasil. {{ horario_hoje }} </p>
            </div>
        
            <hr style="margin-top: 150px;color: #ffffff; width: 50px">
            <div id="ceo">
                <p> Diogo Antonio</p>
                <p> CEO & Desenvolvedor BackEnd</p>
            </div>
        
            <img src="" class="logo-inferior">
        </body>
        </html>
        """

        template = Template(template_contrato)

        locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

        hoje = datetime.datetime.now().date().strftime("%d de %B de %Y")

        rendered_template = template.render(
            carona=carona,
            caroneiro=objeto,
            hoje_str=hoje,
            horario_hoje=horario,
        )

    return rendered_template