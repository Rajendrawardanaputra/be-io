from django.db import models


class ProjectCharter(models.Model):
     project_name = models.CharField(max_length=255, blank=True, null=True)
     project_manager = models.CharField(max_length=255, blank=True, null=True)
     customer = models.CharField(max_length=255, blank=True, null=True)
     end_customer = models.CharField(max_length=255, blank=True, null=True)
     bu_delivery = models.CharField(max_length=255, blank=True, null=True)
     bu_related = models.CharField(max_length=255, blank=True, null=True)
     id_charter = models.AutoField(primary_key=True)
     project_description = models.CharField(max_length=255, blank=True, null=True)
     createdAt = models.DateTimeField(auto_now_add=True)   #Field name made lowercase.
     status_project = models.CharField(max_length=255, choices=[('draft', 'Draft'), ('done', 'Done')], default='draft')
     id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
     updateAt = models.DateTimeField(auto_now=True)   #Field name made lowercase.

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
     createdAt = models.DateTimeField(auto_now_add=True)   #Field name made lowercase.
     updatedAt = models.DateTimeField(auto_now=True)
     status_description = models.TextField(blank=True, null=True)   #This field type is a guess.

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
     createdAt = models.DateTimeField(auto_now_add=True)   #Field name made lowercase.
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
     createdAt = models.DateTimeField(auto_now_add=True)   #Field name made lowercase.
     updatedAt = models.DateTimeField(auto_now=True)
     status_responsibility = models.TextField(blank=True, null=True)   #This field type is a guess.  

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
     createdAt = models.DateTimeField(auto_now_add=True)   #Field name made lowercase.
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
     createdAt = models.DateTimeField(auto_now_add=True)   #Field name made lowercase.
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
     createdAt = models.DateTimeField(auto_now_add=True)   #Field name made lowercase.
     updatedAt = models.DateTimeField(auto_now=True)
     status_detailresponsibilities = models.TextField(blank=True, null=True) 

     class Meta:
         managed = False
         db_table = 'detail_responsibilities'

class Deliverable(models.Model):
     id_deliverable = models.AutoField(primary_key=True)
     deliverables = models.TextField(blank=True, null=True)
     id_charter = models.ForeignKey('ProjectCharter', models.DO_NOTHING, db_column='id_charter', blank=True, null=True)
     id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
     createdAt = models.DateTimeField(auto_now_add=True)   #Field name made lowercase.
     updatedAt = models.DateTimeField(auto_now=True)   #Field name made lowercase.
     status_deliverable = models.TextField(blank=True, null=True)   #This field type is a guess.

     class Meta:
         managed = False
         db_table = 'deliverable'

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



class Status(models.Model):
     id_status = models.AutoField(primary_key=True)
     status = models.TextField(blank=True, null=True)   #This field type is a guess.
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

     def save(self, *args, **kwargs):
        # Ambil status dari setiap atribut terkait
        status_values = [
            self.id_charter.status_project if self.id_charter else None,
            self.id_description.status_description if self.id_description else None,
            self.id_deliverable.status_deliverable if self.id_deliverable else None,
            self.id_milostone.status_milostones if self.id_milostone else None,
            self.id_responsibilities.status_responsibilities if self.id_responsibilities else None,
            self.id_responsibility.status_responsibility if self.id_responsibility else None,
            self.id_supporting.status_supportingdoc if self.id_supporting else None,
            self.id_approv.status_approvedby if self.id_approv else None,
            self.id_detail_roleresponsibilities.status_detailresponsibilities if self.id_detail_roleresponsibilities else None,
        ]

        # Hilangkan nilai-nilai yang bernilai `None` (jika ada)
        status_values = [status for status in status_values if status is not None]

        # Jika ada yang "Draft", maka status keseluruhan adalah "Draft"
        if "draft" in status_values:
            self.status = "Draft"
        # Jika semua status adalah "done", maka status keseluruhan adalah "Done"
        elif all(status.lower() == "done" for status in status_values):
            self.status = "Done"
        # Jika tidak ada yang "Draft" dan tidak semua "Done", maka status keseluruhan adalah None (kosong)
        else:
            self.status = None

        super().save(*args, **kwargs)
        
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
