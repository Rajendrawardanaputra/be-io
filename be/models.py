# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Approvedby(models.Model):
    nama = models.CharField(max_length=255, blank=True, null=True)
    cc_to = models.CharField(max_length=255, blank=True, null=True)
    tanggal = models.DateField(blank=True, null=True)
    id_approv = models.AutoField(primary_key=True)
    note = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    id_charter = models.ForeignKey('ProjectCharter', models.DO_NOTHING, db_column='id_charter', blank=True, null=True)
    id_user = models.IntegerField(blank=True, null=True)
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    status_approvedby = models.TextField(blank=True, null=True)  # This field type is a guess.
    nama1 = models.CharField(max_length=255, blank=True, null=True)
    title1 = models.CharField(max_length=255, blank=True, null=True)
    cc_to1 = models.CharField(max_length=255, blank=True, null=True)
    tanggal1 = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'approvedBy'
