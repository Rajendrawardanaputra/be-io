# Generated by Django 4.2.7 on 2023-12-08 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Description',
            fields=[
                ('hlr', models.FileField(blank=True, max_length=255, null=True, upload_to='hlr/')),
                ('assumptions', models.CharField(blank=True, max_length=50, null=True)),
                ('contraints', models.CharField(blank=True, max_length=50, null=True)),
                ('risk', models.CharField(blank=True, max_length=50, null=True)),
                ('key_stakeholders', models.CharField(blank=True, max_length=50, null=True)),
                ('id_description', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'description',
                'managed': False,
            },
        ),
    ]
