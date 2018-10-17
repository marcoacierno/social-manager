from django.contrib import admin, messages
from django.shortcuts import redirect, render
from django.urls import path, reverse

from providers import get_all_providers

from .models import Metadata, Post


class MetadataInline(admin.StackedInline):
    model = Metadata

    def has_add_permission(self, request):
        return False


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    ordering = ("status",)
    list_display = ("title", "status")
    inlines = [MetadataInline]
    fieldsets = (("Post", {"fields": ("title", "content", "status")}),)
    readonly_fields = ("status",)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "<int:object_id>/publish/",
                self.admin_site.admin_view(self.publish_recap),
                name="publish_recap",
            )
        ]
        return my_urls + urls

    def response_change(self, request, obj):
        if "_publish" in request.POST:
            return redirect(reverse("admin:publish_recap", args=[obj.id]))

        return super().response_change(request, obj)

    def publish_recap(self, request, object_id):
        post = Post.objects.get(id=object_id)

        if request.method == "POST":
            response = redirect(reverse("admin:posts_post_change", args=[object_id]))

            if "_publish" in request.POST:
                messages.success(request, "Post schedulated for publishing!")
                post.publish()

            return response

        socials = []

        for provider in get_all_providers():
            if not provider.is_active:
                continue

            already_exists = Metadata.objects.filter(
                post=post,
                provider_name=provider.NAMESPACE,
                status=Metadata.STATUS.created,
            ).exists()

            socials.append(
                {"name": provider.NAMESPACE, "already_exists": already_exists}
            )

        return render(
            request,
            "admin/posts/publish.html",
            context=dict(
                self.admin_site.each_context(request), post=post, socials=socials
            ),
        )
