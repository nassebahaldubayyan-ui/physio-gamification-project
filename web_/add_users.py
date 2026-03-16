import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import Users
from django.contrib.auth.hashers import make_password

print("="*50)
print("🔍 ADDING USERS TO DATABASE")
print("="*50)

count = Users.objects.count()
print(f"📊 Current users: {count}")

if count > 0:
    Users.objects.all().delete()
    print("🗑️ Deleted existing users")

users = [
    {'name': 'Ali Ahmed', 'email': 'ali@rehab.com', 'password': '123456', 'role': 'patient'},
    {'name': 'Sara Khaled', 'email': 'sara@rehab.com', 'password': '123456', 'role': 'patient'},
    {'name': 'Omar Hassan', 'email': 'omar@rehab.com', 'password': '123456', 'role': 'patient'},
    {'name': 'Dr. Ahmad', 'email': 'dr.ahmad@clinic.com', 'password': '123456', 'role': 'doctor'},
]

for user_data in users:
    user_data['password'] = make_password(user_data['password'])
    user = Users.objects.create(**user_data)
    print(f"✅ Added: {user.name} - {user.email}")

print(f"\n✅ Total users now: {Users.objects.count()}")
print("="*50)