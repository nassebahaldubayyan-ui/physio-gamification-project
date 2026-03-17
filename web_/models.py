# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Doctors(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING)
    doctor_id = models.TextField(unique=True)
    specialty = models.TextField()
    license_number = models.TextField(unique=True)
    hospital = models.TextField()
    experience = models.IntegerField(blank=True, null=True)
    available = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doctors'


class GameSessions(models.Model):
    patient = models.ForeignKey('Patients', models.DO_NOTHING)
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
    session_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'game_sessions'


class Messages(models.Model):
    sender_id = models.IntegerField()
    sender_type = models.TextField()
    receiver_id = models.IntegerField()
    receiver_type = models.TextField()
    content = models.TextField()
    is_read = models.IntegerField(blank=True, null=True)
    read_at = models.TextField(blank=True, null=True)  # This field type is a guess.
    created_at = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'messages'


class Patients(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    patient_id = models.TextField(unique=True)
    date_of_birth = models.DateField()
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
    wrist_strength = models.IntegerField(blank=True, null=True)
    grip_strength = models.IntegerField(blank=True, null=True)
    external_rotation = models.IntegerField(blank=True, null=True)
    affected_hand = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patients'


class Users(models.Model):
    name = models.TextField()
    email = models.TextField(unique=True)
    password = models.TextField()
    role = models.TextField()
    phone = models.TextField()
    avatar = models.TextField(blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    last_login = models.TextField(blank=True, null=True)  # This field type is a guess.
    created_at = models.TextField(blank=True, null=True)  # This field type is a guess.
    updated_at = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'users'
