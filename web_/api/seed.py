import os
import django
from django.contrib.auth.hashers import make_password

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import Users

def seed_users():
    print("Adding users to database...")
    
    users = [
        {
            'name': 'Ali Ahmed',
            'email': 'ali@rehab.com',
            'password': make_password('123456'),
            'role': 'patient',
            'phone': '0501111111'
        },
        {
            'name': 'Sara Khaled',
            'email': 'sara@rehab.com',
            'password': make_password('123456'),
            'role': 'patient',
            'phone': '0502222222'
        },
        {
            'name': 'Omar Hassan',
            'email': 'omar@rehab.com',
            'password': make_password('123456'),
            'role': 'patient',
            'phone': '0503333333'
        },
        {
            'name': 'Dr. Ahmad',
            'email': 'dr.ahmad@clinic.com',
            'password': make_password('123456'),
            'role': 'doctor',
            'phone': '0504444444'
        }
    ]
    
    for user_data in users:
        user = Users.objects.create(**user_data)
        print(f"✅ Added: {user_data['name']}")
    
    print("\n✅ All users added successfully!")

if __name__ == '__main__':
    seed_users()