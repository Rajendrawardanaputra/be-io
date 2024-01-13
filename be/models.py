# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Status(models.Model):
    id_status = models.AutoField(primary_key=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_description = models.ForeignKey('Description', models.DO_NOTHING, db_column='id_description', blank=True, null=True)
    id_deliverable = models.ForeignKey('Deliverable', models.DO_NOTHING, db_column='id_deliverable', blank=True, null=True)
    id_milostone = models.ForeignKey('Milostones', models.DO_NOTHING, db_column='id_milostone', blank=True, null=True)
    id_responsibilities = models.ForeignKey('RoleResponsibilities', models.DO_NOTHING, db_column='id_responsibilities', blank=True, null=True)
    id_responsibility = models.ForeignKey('Responsibility', models.DO_NOTHING, db_column='id_responsibility', blank=True, null=True)
    id_supporting = models.ForeignKey('SupportingDoc', models.DO_NOTHING, db_column='id_supporting', blank=True, null=True)
    id_approv = models.ForeignKey('Approvedby', models.DO_NOTHING, db_column='id_approv', blank=True, null=True)
    id_charter = models.ForeignKey('ProjectCharter', models.DO_NOTHING, db_column='id_charter', blank=True, null=True)
    id_detail_roleresponsibilities = models.ForeignKey('DetailResponsibilities', models.DO_NOTHING, db_column='id_detail_roleresponsibilities', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'status'
