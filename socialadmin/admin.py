from django.contrib import admin


class SocialAdmin(admin.AdminSite):
    index_template = "socialadmin/admin_index.html"
