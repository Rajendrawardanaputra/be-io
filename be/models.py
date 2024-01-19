# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ProjectInternal(models.Model):
    id_project = models.AutoField(primary_key=True)
    requester = models.TextField(blank=True, null=True)
    application_name = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    hld = models.TextField(blank=True, null=True)
    lld = models.TextField(blank=True, null=True)
    brd = models.TextField(blank=True, null=True)
    sequence_number = models.CharField(max_length=20, blank=True, null=True)
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updateat = models.DateTimeField(db_column='updateAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'project_internal'
