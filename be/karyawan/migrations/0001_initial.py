# Generated by Django 4.2.7 on 2023-11-17 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Karyawan',
            fields=[
                ('id_karyawan', models.AutoField(primary_key=True, serialize=False)),
                ('id_role', models.CharField(max_length=10)),
                ('nama_karyawan', models.CharField(max_length=255)),
                ('jabatan', models.CharField(max_length=255)),
                ('nomor_telepon', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
    ]
