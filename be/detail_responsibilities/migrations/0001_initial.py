# Generated by Django 4.2.7 on 2023-12-08 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DetailResponsibilities',
            fields=[
                ('id_detail_roleresponsibilities', models.AutoField(primary_key=True, serialize=False)),
                ('nama_pc', models.CharField(blank=True, max_length=255, null=True)),
                ('role_pc', models.CharField(blank=True, max_length=255, null=True)),
                ('responsibilities', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'detail_responsibilities',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RoleResponsibilities',
            fields=[
                ('struktur_organisasi', models.FileField(blank=True, max_length=255, null=True, upload_to='struktur/')),
                ('id_responsibilities', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'role_responsibilities',
                'managed': False,
            },
        ),
    ]
