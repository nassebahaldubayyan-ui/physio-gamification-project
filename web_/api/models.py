from django.db import models
from django.contrib.auth.hashers import check_password, make_password

class Users(models.Model):
    id = models.AutoField(primary_key=True)  
    name = models.TextField()
    email = models.TextField(unique=True)
    password = models.TextField()
    role = models.TextField()
    phone = models.TextField()
    avatar = models.TextField(blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True, default=1)
    last_login = models.TextField(blank=True, null=True)
    created_at = models.TextField(blank=True, null=True)
    updated_at = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
    
    def __str__(self):
        return self.name
    
    def verify_password(self, raw_password):
        return check_password(raw_password, self.password)


class Patients(models.Model):
    user = models.OneToOneField(Users, on_delete=models.DO_NOTHING)
    patient_id = models.TextField(unique=True)
    date_of_birth = models.TextField()
    gender = models.TextField()
    medical_condition = models.TextField()
    therapy_type = models.TextField()
    current_level = models.IntegerField(blank=True, null=True)
    assigned_doctor_id = models.IntegerField(blank=True, null=True)
    emergency_contact_name = models.TextField(blank=True, null=True)
    emergency_contact_phone = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    shoulder_strength = models.IntegerField(blank=True, null=True)
    elbow_strength = models.IntegerField(blank=True, null=True)
    grip_strength = models.IntegerField(blank=True, null=True)
    affected_hand = models.TextField()
    photo_url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patients'
    
    def __str__(self):
        return f"Patient: {self.user.name}"


class Doctors(models.Model):
    user = models.OneToOneField(Users, on_delete=models.DO_NOTHING)
    doctor_id = models.TextField(unique=True)
    specialty = models.TextField()
    license_number = models.TextField(unique=True)
    hospital = models.TextField()
    experience = models.IntegerField(blank=True, null=True)
    available = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doctors'
    
    def __str__(self):
        return f"Dr. {self.user.name}"


class GameSessions(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.DO_NOTHING)
    game_type = models.TextField()
    level = models.IntegerField()
    score = models.IntegerField()
    duration = models.IntegerField()
    accuracy = models.IntegerField(blank=True, null=True)
    stars_caught = models.IntegerField(blank=True, null=True)
    matches_made = models.IntegerField(blank=True, null=True)
    objects_caught = models.IntegerField(blank=True, null=True)
    shoulder_activation = models.IntegerField(blank=True, null=True)
    elbow_activation = models.IntegerField(blank=True, null=True)
    wrist_activation = models.IntegerField(blank=True, null=True)
    grip_activation = models.IntegerField(blank=True, null=True)
    external_rotation = models.IntegerField(blank=True, null=True)
    shoulder_shrug = models.IntegerField(blank=True, null=True)
    completed = models.IntegerField(blank=True, null=True)
    session_date = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'game_sessions'
    
    def __str__(self):
        return f"Session {self.id} - {self.game_type}"


class Messages(models.Model):
    sender_id = models.IntegerField()
    sender_type = models.TextField()
    receiver_id = models.IntegerField()
    receiver_type = models.TextField()
    content = models.TextField()
    is_read = models.IntegerField(blank=True, null=True, default=0)
    read_at = models.TextField(blank=True, null=True)
    created_at = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'messages'
    
    def __str__(self):
        return f"Message {self.id}"