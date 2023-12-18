# Generated by Django 4.2.5 on 2023-10-08 20:48
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='connection',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('process', models.CharField(max_length=25)),
                ('action', models.CharField(max_length=25, null=True)),
                ('server', models.CharField(max_length=250)),
                ('port', models.IntegerField(null=True)),
                ('method', models.CharField(max_length=10)),
                ('headers', models.TextField(null=True)),
                ('params', models.TextField(null=True)),
                ('body', models.TextField(null=True)),
                ('createdon', models.DateTimeField(null=False)),
                ('createdby', models.CharField(max_length=50, null=True)),
                ('ind_activo', models.SmallIntegerField(default=1)),
                ('modifiedon', models.DateTimeField(null=True)),
                ('modifiedby', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'connections',
            },
        ),
        migrations.CreateModel(
            name='eventlog',
            fields=[
                ('rowid', models.AutoField(primary_key=True, serialize=False)),
                ('process', models.CharField(max_length=30)),
                ('action', models.CharField(max_length=30)),
                ('rowid_entity', models.IntegerField(default=0)),
                ('userid', models.CharField(max_length=30)),
                ('regdate', models.DateTimeField(auto_now_add=True)),
                ('request', models.TextField()),
                ('response', models.TextField(null=True)),
                ('errors', models.TextField(null=True)),
            ],
            options={
                'db_table': 'eventlogs',
            },
        ),
    ]
