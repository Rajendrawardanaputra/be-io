from django.db import models

class ActivityLog(models.Model):
    id_activity_log = models.AutoField(primary_key=True)
    detail_activity = models.CharField(max_length=255, blank=True, null=True)
    action_activity = models.TextField(blank=True, null=True)
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    timestampz = models.DateTimeField(auto_now_add=True)
    id_project = models.ForeignKey('ProjectInternal', models.DO_NOTHING, db_column='id_project', blank=True, null=True)
    id_role = models.ForeignKey('DetailMainPower', models.DO_NOTHING, db_column='id_role', blank=True, null=True)
    id_detail_timeline = models.ForeignKey('DetailTimeline', models.DO_NOTHING, db_column='id_detail_timeline', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'activity_log'

    def __str__(self):
        return f"{self.timestampz} | {self.id_user.nama if self.id_user else 'Unknown User'} | {self.action_activity} | {self.detail_activity}"

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

class ProjectStatus(models.TextChoices):
    ON_GOING = 'ON_GOING', 'Ongoing'
    DROPPED = 'DROPPED', 'Dropped'
    FINISH = 'FINISH', 'Finish'

class ProjectInternal(models.Model):
    id_project = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.ON_GOING)
    requester = models.CharField(max_length=100, blank=True, null=True)
    application_name = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    hld = models.ImageField(upload_to='internalorder/', max_length=255, null=True, blank=True)
    lld = models.ImageField(upload_to='internalorder/', max_length=255, null=True, blank=True)
    brd = models.URLField(max_length=255, blank=True, null=True)
    sequence_number = models.CharField(max_length=20, blank=True, null=True)
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False 
        db_table = 'project_internal'

class DetailMainPower(models.Model):
    id_role = models.AutoField(primary_key=True)
    man_days_rate = models.IntegerField(blank=True, null=True)
    man_power = models.IntegerField(blank=True, null=True)
    days = models.IntegerField(blank=True, null=True)
    role = models.TextField(blank=True, null=True)
    total_man_rate = models.IntegerField(blank=True, null=True)
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    id_project = models.ForeignKey('ProjectInternal', models.DO_NOTHING, db_column='id_project', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detail_main_power'

class DetailTimeline(models.Model):
    id_detail_timeline = models.AutoField(primary_key=True)
    weeks = models.IntegerField(blank=True, null=True)
    activity = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    id_project = models.ForeignKey('ProjectInternal', models.DO_NOTHING, db_column='id_project', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detail_timeline'
