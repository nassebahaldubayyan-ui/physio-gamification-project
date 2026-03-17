from django.db import models

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, default='patient')  # patient, doctor
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.CharField(max_length=255, default='default-avatar.png')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return f"{self.name} ({self.email})"


#Patient
class Patient(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)  
    condition = models.CharField(max_length=255)
    therapy = models.CharField(max_length=255)
    level = models.IntegerField()

    class Meta:
        db_table = 'patients'

    def __str__(self):
        return f"{self.user.name} - {self.condition} - Level {self.level}"


#Doctor
class Doctor(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=255)
    experience_years = models.IntegerField()

    class Meta:
        db_table = 'doctors'

    def __str__(self):
        return f"Dr. {self.user.name} - {self.specialty} ({self.experience_years} years of experience)"


class Messages(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'messages'

    def __str__(self):
        return f"Message from {self.sender.name} to {self.receiver.name}"