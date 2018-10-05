from django.contrib.admin.apps import AdminConfig


class SocialAdminConfig(AdminConfig):
    default_site = "socialadmin.admin.SocialAdmin"
