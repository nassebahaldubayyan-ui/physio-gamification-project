from django.db import models
from django.utils import timezone

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    avatar = models.CharField(max_length=255)
    is_active = models.IntegerField(blank=True, null=True)
    last_login = models.TextField(blank=True, null=True)
    created_at = models.TextField(blank=True, null=True)
    updated_at = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return self.name


class Patients(models.Model):
    user = models.OneToOneField(Users, models.DO_NOTHING)
    patient_id = models.TextField(unique=True)
    date_of_birth = models.TextField()
    gender = models.TextField()
    medical_condition = models.TextField()
    therapy_type = models.TextField()
    stars_level = models.IntegerField(blank=True, null=True, default=1)
    falling_level = models.IntegerField(blank=True, null=True, default=1)
    matching_level = models.IntegerField(blank=True, null=True, default=1)
    assigned_doctor_id = models.IntegerField(blank=True, null=True)
    emergency_contact_name = models.TextField(blank=True, null=True)
    emergency_contact_phone = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    shoulder_strength = models.IntegerField(blank=True, null=True)
    shoulder_external_strength = models.IntegerField(blank=True, null=True)
    elbow_strength = models.IntegerField(blank=True, null=True)
    grip_strength = models.IntegerField(blank=True, null=True)
    affected_hand = models.TextField()
    photo_url = models.TextField(blank=True, null=True)

    
    # NEW FIELD - For tracking assessment video
    has_assessment_video = models.IntegerField(blank=True, null=True, default=0)
    assessment_date = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patients'

    def __str__(self):
        return f"Patient: {self.user.name}"


class Doctors(models.Model):
    user = models.OneToOneField(Users, models.DO_NOTHING)
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


class Messages(models.Model):
    id = models.AutoField(primary_key=True)
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


class GameSessions(models.Model):
    patient = models.ForeignKey(Patients, models.DO_NOTHING)
    user_id = models.IntegerField(blank=True, null=True)
    player_name= models.TextField(blank=True, null=True)
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
    session_date = models.DateTimeField(blank=True, null=True)
    pain_score = models.IntegerField(null=True, blank=True)
    enjoyment_score = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'game_sessions'

    def __str__(self):
        return f"Session {self.id} - {self.game_type}"