from django.db import models

class Users(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20)  # patient, doctor, gamer
    phone = models.CharField(max_length=15, blank=True)
    avatar = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.name} - {self.role}"


class Doctor(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='doctor_profiles')
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)
    years_experience = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'doctor'

    def __str__(self):
        return f"Dr. {self.user.name} - {self.specialization}"


class Patient(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='patient_profiles')
    date_of_birth = models.DateField(null=True, blank=True)
    medical_history = models.TextField(blank=True)
    assigned_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    current_level = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'patient'

    def __str__(self):
        return f"Patient: {self.user.name}"


class Game(models.Model):
    name = models.CharField(max_length=100)
    game_type = models.CharField(max_length=50)  # catching_stars, matching, catching_objects
    description = models.TextField(blank=True)
    difficulty_level = models.IntegerField(default=1)
    thumbnail = models.CharField(max_length=255, blank=True)
    game_file = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'game'

    def __str__(self):
        return self.name


class GameSession(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='game_sessions')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.IntegerField(default=0)
    duration_seconds = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'game_session'

    def __str__(self):
        return f"{self.patient.user.name} - {self.game.name} - {self.score}"


class Messages(models.Model):
    sender = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'messages'

    def __str__(self):
        return f"From {self.sender.name} to {self.receiver.name}"