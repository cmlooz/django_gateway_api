import json
from django.db import models


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


class eventlog(models.Model):
    rowid = models.AutoField(primary_key=True)
    process = models.CharField(max_length=30, null=False)
    action = models.CharField(max_length=30, null=False)
    rowid_entity = models.IntegerField(default=0)
    userid = models.CharField(max_length=30, null=False)
    regdate = models.DateTimeField(auto_now_add=True)
    request = models.TextField(null=False)
    response = models.TextField(null=True)
    errors = models.TextField(null=True)

    class Meta:
        db_table = 'eventlogs'

    def __str__(self):
        regdate_str = self.regdate.strftime('%Y-%m-%d %h:%m:%s')

        return json.dumps({
            "rowid": self.rowid,
            "process": self.process,
            "action": self.action,
            "rowid_entity": self.rowid_entity,
            "userid": self.userid,
            "regdate": regdate_str,
            "request": self.request,
            "response": self.response,
            "errors": self.errors
        })
