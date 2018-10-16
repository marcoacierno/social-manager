from django.contrib import admin

from .models import Metadata, Post


class MetadataInline(admin.TabularInline):
    model = Metadata


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    ordering = ("status",)
    list_display = ("title", "status")
    inlines = []
    fieldsets = (("Post", {"fields": ("title", "content", "status")}),)
    readonly_fields = ("status",)

    def get_fieldsets(self, request, obj=None):
        if obj.status == Post.STATUS.published:
            return super().get_fieldsets(request, obj) + [MetadataInline]

        return super().get_fieldsets(request, obj)

    def save_form(self, request, form, change):
        if "_publish" in form.data:
            form.instance.publish()

        return super().save_form(request, form, change)
