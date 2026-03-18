from django.db import models

class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10)  # 'patient' or 'doctor'
    phone = models.CharField(max_length=20)
    avatar = models.CharField(max_length=255, default='default-avatar.png')
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        managed = False  # Don't let Django modify the table

    def __str__(self):
        return self.name


class Messages(models.Model):
    id = models.IntegerField(primary_key=True)
    sender_id = models.IntegerField()
    receiver_id = models.IntegerField()
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'messages'
        managed = False

    def __str__(self):
        return f"Message {self.id}"
