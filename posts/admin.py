from django.contrib import admin

from .models import Metadata, Post


class MetadataInline(admin.TabularInline):
    model = Metadata


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    ordering = ("status",)
    list_display = ("title", "status")
    inlines = [MetadataInline]
    fieldsets = (("Post", {"fields": ("title", "content", "status")}),)
    readonly_fields = ("status",)

    def save_form(self, request, form, change):
        if "_publish" in form.data:
            form.instance.publish()

        return super().save_form(request, form, change)
