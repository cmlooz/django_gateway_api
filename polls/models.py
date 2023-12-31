import json
from django.db import models

# Create your models here.


class connection(models.Model):
    name = models.CharField(max_length=50)
    process = models.CharField(max_length=25, null=True)
    action = models.CharField(max_length=25, null=True)
    server = models.CharField(max_length=250)
    port = models.IntegerField(null=True)
    method = models.CharField(max_length=10, null=True)
    headers = models.TextField(null=True)
    params = models.TextField(null=True)
    body = models.TextField(null=True)
    createdon = models.DateTimeField(null=True)
    createdby = models.CharField(max_length=50, null=True)
    ind_activo = models.SmallIntegerField(default=1)
    modifiedon = models.DateTimeField(null=True)
    modifiedby = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'connections'

    def __str__(self):
        try:
            modifiedon_str = self.modifiedon.strftime('%Y-%m-%d')
        except AttributeError:
            modifiedon_str = None

        createdon_str = self.createdon.strftime('%Y-%m-%d')

        return json.dumps({
            "id": self.id,
            "name": self.name,
            "process": self.process,
            "action": self.action,
            "server": self.server,
            "port": self.port,
            "method": self.method,
            "headers": self.headers,
            "params": self.params,
            "body": self.body,
            "createdon": createdon_str,
            "createdby": self.createdby,
            "ind_activo": self.ind_activo,
            "modifiedby": self.modifiedby,
            "modifiedon": modifiedon_str
        })
