from django.contrib import admin

# Register your models here.
from .models import connection


class connectionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name", "method", "server", "port", "process", "action", "params", "headers",
                           "body", "modifiedon", "modifiedby"]}),
        ("Date information", {"fields": [
         "createdon", "createdby", "ind_activo"]}),
    ]
    list_display = ["id", "name", "method", "server", "port", "process",
                    "action", "params", "headers", "body", "createdon", "createdby"]


admin.site.register(connection, connectionAdmin)
