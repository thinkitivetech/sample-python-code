from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .models import Organisation, Report

# Register your models here.


# admin.site.register(Organisation)
# admin.site.register(Report)


@admin.register(Organisation)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "canonical_domain", "date_created"]


@admin.register(Report)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "organisation_id",
        "created",
        "completed",
        "cyberrisk",
        "result",
    ]
