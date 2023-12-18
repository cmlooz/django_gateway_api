from django.contrib import admin

# Register your models here.
from .models import connection
from .models import eventlog


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


class eventlogAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["process",
                           "action",
                           "rowid_entity",
                           "request",
                           "response",
                           "errors"]}),
        ("Date information", {"fields": [
         "userid"]}),
    ]
    list_display = ["rowid",
                    "process",
                    "action",
                    "rowid_entity",
                    "request",
                    "response",
                    "errors",
                    "regdate",
                    "userid"]


admin.site.register(eventlog, eventlogAdmin)
