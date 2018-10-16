from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from . import get_provider


def provider_pages_index(request, slug):
    provider = get_provider(slug)

    if request.method.lower() == "post":
        success = provider.set_active_page(**request.POST)

        if not success:
            messages.error(request, "Unable to change the active page")
        else:
            messages.success(request, "Changed!")

        return redirect(reverse("admin:index"))

    context = {"pages": provider.pages, "active_page": provider.active_page}

    return render(request, "provider/pages_list.html", context=context)
