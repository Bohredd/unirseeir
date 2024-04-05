from functools import wraps
from django.shortcuts import redirect


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


def is_conta_do_requester():
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            user_id = kwargs.get("id")
            print("passado:", user_id)
            print("requester: ", request.user.id)
            if request.user.is_authenticated:
                if str(request.user.id) == str(user_id):
                    return view_func(request, *args, **kwargs)
            return redirect("home")

        return wrapped_view

    return decorator
