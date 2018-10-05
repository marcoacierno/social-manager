from . import PROVIDERS


def providers(request):
    return {"providers": PROVIDERS}
