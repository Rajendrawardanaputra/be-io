from django.db import models

class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    password = models.CharField(max_length=255)
    hak_akses = models.TextField(blank=True, null=True)
    nama = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    jabatan = models.CharField(max_length=255, blank=True, null=True)
    profile = models.ImageField(upload_to='internalorder/', max_length=255, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'user'

class ProjectCharter(models.Model):
    project_name = models.CharField(blank=True, null=True)
    project_manager = models.CharField(blank=True, null=True)
    customer = models.CharField(blank=True, null=True)
    end_customer = models.CharField(blank=True, null=True)
    bu_delivery = models.CharField(blank=True, null=True)
    bu_related = models.CharField(blank=True, null=True)
    id_charter = models.AutoField(primary_key=True)
    project_description = models.CharField(max_length=255, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)  # Field name made lowercase.
    status_project = models.CharField(max_length=255, blank=True, null=True)
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    updateAt = models.DateTimeField(auto_now=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'project_charter'


class Approvedby(models.Model):
    nama = models.CharField(max_length=255, blank=True, null=True)
    cc_to = models.CharField(max_length=255, blank=True, null=True)
    tanggal = models.DateField(blank=True, null=True)
    id_approv = models.AutoField(primary_key=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    id_charter = models.ForeignKey('ProjectCharter', models.DO_NOTHING, db_column='id_charter', blank=True, null=True)
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)  # Field name made lowercase.
    updatedAt = models.DateTimeField(auto_now=True)
    status_approvedby = models.TextField(blank=True, null=True)
    nama1 = models.CharField(max_length=255, blank=True, null=True)
    title1 = models.CharField(max_length=255, blank=True, null=True)
    cc_to1 = models.CharField(max_length=255, blank=True, null=True)
    tanggal1 = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'approvedBy'