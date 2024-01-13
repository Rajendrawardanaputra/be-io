# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ProjectCharter(models.Model):
    project_name = models.CharField(blank=True, null=True)
    project_manager = models.CharField(blank=True, null=True)
    customer = models.CharField(blank=True, null=True)
    end_customer = models.CharField(blank=True, null=True)
    bu_delivery = models.CharField(blank=True, null=True)
    bu_related = models.CharField(blank=True, null=True)
    id_charter = models.AutoField(primary_key=True)
    project_description = models.TextField(blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    id_user = models.IntegerField(blank=True, null=True)
    updateat = models.DateTimeField(db_column='updateAt', blank=True, null=True)  # Field name made lowercase.
    status_project = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'project_charter'
