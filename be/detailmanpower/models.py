# models.py

from django.db import models


class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    password = models.CharField(max_length=255)
    hak_akses = models.TextField(blank=True, null=True)
    nama = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    jabatan = models.CharField(max_length=255, blank=True, null=True)
    profile = models.FileField(upload_to='profiles/', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
        
class ProjectStatus(models.TextChoices):
    ON_GOING = 'on_going', 'Ongoing'
    DROPPED = 'dropped', 'Dropped'
    FINISH = 'finish', 'Finish'

class ProjectInternal(models.Model):
    id_project = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.ON_GOING)
    requester = models.CharField(max_length=100, blank=True, null=True)
    application_name = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    hld = models.FileField(upload_to='hld/', max_length=255, blank=True, null=True)
    lld = models.FileField(upload_to='lld/', max_length=255, blank=True, null=True)
    brd = models.URLField(max_length=255, blank=True, null=True)
    sequence_number = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_internal'


class DetailMainPower(models.Model):
    id_role = models.AutoField(primary_key=True)
    man_days_rate = models.IntegerField(blank=True, null=True)
    man_power = models.IntegerField(blank=True, null=True)
    days = models.IntegerField(blank=True, null=True)
    role = models.TextField(blank=True, null=True)  # This field type is a guess.
    total_man_rate = models.IntegerField(blank=True, null=True)
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    id_project = models.ForeignKey('ProjectInternal', models.DO_NOTHING, db_column='id_project', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detail_main_power'
        

