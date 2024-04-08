from functools import wraps
from django.shortcuts import redirect
from core.models import Carona
from django.contrib import messages


def is_tipo(tipo_permitido):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and hasattr(request.user, "tipo_ativo"):
                if request.user.tipo_ativo in tipo_permitido:
                    return view_func(request, *args, **kwargs)
            return redirect("home")

        return wrapped_view

    return decorator


def user_in_carona():

    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):

            carona_id = request.path.split("carona/ver/")[1].split("/")[0]

            if carona_id:
                carona = Carona.objects.filter(pk=carona_id)
                if carona.exists():

                    carona = carona.first()
                    if (
                        carona.caroneiros.all().filter(user=request.user).exists()
                        or carona.motorista == request.user
                    ):
                        return view_func(request, *args, **kwargs)

            messages.error(request, "Você não tem permissão para isso!")
            return redirect("home")

        return wrapped_view

    return decorator
