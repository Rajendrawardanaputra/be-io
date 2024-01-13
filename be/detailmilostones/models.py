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

class Description(models.Model):
    hlr = models.FileField(max_length=255, blank=True, null=True)
    assumptions = models.CharField(max_length=255, blank=True, null=True)
    contraints = models.CharField(max_length=255, blank=True, null=True)
    risk = models.CharField(max_length=255, blank=True, null=True)
    key_stakeholders = models.CharField(max_length=255, blank=True, null=True)
    id_description = models.AutoField(primary_key=True)
    id_charter = models.ForeignKey('ProjectCharter', models.DO_NOTHING, db_column='id_charter', blank=True, null=True)
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)  # Field name made lowercase.
    updatedAt = models.DateTimeField(auto_now=True)
    status_description = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'description'

class SupportingDoc(models.Model):
    document_name = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    document = models.FileField(max_length=255, blank=True, null=True)
    id_supporting = models.AutoField(primary_key=True)
    id_charter = models.ForeignKey('ProjectCharter', models.DO_NOTHING, db_column='id_charter', blank=True, null=True)
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)  # Field name made lowercase.
    updatedAt = models.DateTimeField(auto_now=True)
    status_supportingdoc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'supporting_doc'


class Responsibility(models.Model):
    pm_responsibility = models.TextField(blank=True, null=True)
    project_value = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    id_responsibility = models.AutoField(primary_key=True)
    id_charter = models.ForeignKey('ProjectCharter', models.DO_NOTHING, db_column='id_charter', blank=True, null=True)
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)  # Field name made lowercase.
    updatedAt = models.DateTimeField(auto_now=True)
    status_responsibility = models.TextField(blank=True, null=True)  # This field type is a guess.  

    class Meta:
        managed = False
        db_table = 'responsibility'

class Milostones(models.Model):
    milestone = models.TextField(blank=True, null=True)
    deskripsi = models.TextField(blank=True, null=True)
    id_milostone = models.AutoField(primary_key=True)
    tanggal = models.CharField(max_length=255, blank=True, null=True)
    id_charter = models.ForeignKey('ProjectCharter', models.DO_NOTHING, db_column='id_charter', blank=True, null=True)
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)  # Field name made lowercase.
    updatedAt = models.DateTimeField(auto_now=True) 
    status_milostones = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'milostones'

class RoleResponsibilities(models.Model):
    struktur_organisasi = models.ImageField(max_length=255, blank=True, null=True)
    id_responsibilities = models.AutoField(primary_key=True)
    id_charter = models.ForeignKey('ProjectCharter', models.DO_NOTHING, db_column='id_charter', blank=True, null=True)
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)  # Field name made lowercase.
    updatedAt = models.DateTimeField(auto_now=True)
    status_responsibilities = models.TextField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'role_responsibilities'


class DetailResponsibilities(models.Model):
    id_detail_roleresponsibilities = models.AutoField(primary_key=True)
    id_responsibilities = models.ForeignKey('RoleResponsibilities', models.DO_NOTHING, db_column='id_responsibilities', blank=True, null=True)
    nama_pc = models.CharField(max_length=255, blank=True, null=True)
    role_pc = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    id_charter = models.ForeignKey('ProjectCharter', models.DO_NOTHING, db_column='id_charter', blank=True, null=True)
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)  # Field name made lowercase.
    updatedAt = models.DateTimeField(auto_now=True)
    status_detailresponsibilities = models.TextField(blank=True, null=True) 

    class Meta:
        managed = False
        db_table = 'detail_responsibilities'