import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import Users
from django.contrib.auth.hashers import make_password

def add_users():
    users_data = [
        {
            'name': 'Ali Ahmed',
            'email': 'ali@rehab.com',
            'password': '123456',
            'role': 'patient',
            'phone': '0500000000',
            'avatar': 'default-avatar.png'
        },
        {
            'name': 'Dr. Ahmad',
            'email': 'dr.ahmad@clinic.com',
            'password': '123456',
            'role': 'doctor',
            'phone': '0501111111',
            'avatar': 'default-avatar.png'
        },
        {
            'name': 'Sara Khaled',
            'email': 'sara@rehab.com',
            'password': '123456',
            'role': 'patient',
            'phone': '0502222222',
            'avatar': 'default-avatar.png'
        }
    ]
    
    for user_data in users_data:
        user = Users.objects.create(
            name=user_data['name'],
            email=user_data['email'],
            password=make_password(user_data['password']),
            role=user_data['role'],
            phone=user_data['phone'],
            avatar=user_data['avatar'],
            is_active=True
        )
        print(f"✅ Created: {user.name} ({user.email})")

if __name__ == '__main__':
    add_users()
    print("🎯 All users added successfully!")