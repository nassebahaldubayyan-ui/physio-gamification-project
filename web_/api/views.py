from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from .models import Users, Messages
import json

# ========== HTML PAGES ==========

# Main Pages
def index(request):
    return render(request, 'index.html')

def gamer_login(request):
    return render(request, 'gamer-login.html')

def doctor_login(request):
    return render(request, 'doctor-login.html')

def profile(request):
    return render(request, 'profile.html')

def settings(request):
    return render(request, 'settings.html')

def select_patient(request):
    return render(request, 'select-patient.html')

# Patient Pages
def patient_dashboard(request):
    return render(request, 'patient/patient.html')

def patient_chat(request):
    return render(request, 'patient/patient-chat.html')

def patient_game(request):
    return render(request, 'patient/patient-game.html')

def patient_result(request):
    return render(request, 'patient/patient-result.html')

def edit_patient_profile(request):
    return render(request, 'patient/edit-patient-profile.html')

# Doctor Pages
def doctor_dashboard(request):
    return render(request, 'doctor/doctor.html')

def doctor_patients(request):
    return render(request, 'doctor/doctor-patients.html')

def doctor_patient_details(request):
    return render(request, 'doctor/doctor-patient-details.html')

def doctor_messages(request):
    return render(request, 'doctor/doctor-messages.html')

def doctor_performance(request):
    return render(request, 'doctor/doctor-performance.html')

def edit_doctor_profile(request):
    return render(request, 'doctor/edit-doctor-profile.html')

# Game Pages
def game_catching_stars(request):
    return render(request, 'games/game-catching-stars.html')

def game_catching_objects(request):
    return render(request, 'games/game-catching-objects.html')

def game_matching(request):
    return render(request, 'games/game-matching.html')


# ========== APIs ==========

@csrf_exempt
def api_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")
            
            try:
                user = Users.objects.get(email=email, is_active=True)
                if check_password(password, user.password):
                    return JsonResponse({
                        "success": True,
                        "message": "Login successful",
                        "user": {
                            "id": user.id,
                            "name": user.name,
                            "email": user.email,
                            "role": user.role,
                            "phone": user.phone,
                            "avatar": user.avatar
                        }
                    })
                else:
                    return JsonResponse({"success": False, "error": "Wrong password"}, status=401)
            except Users.DoesNotExist:
                return JsonResponse({"success": False, "error": "User not found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def api_register(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            email = data.get("email")
            password = data.get("password")
            role = data.get("role", "patient")
            phone = data.get("phone", "")
            
            if Users.objects.filter(email=email).exists():
                return JsonResponse({"success": False, "error": "Email already exists"}, status=400)
            
            user = Users.objects.create(
                name=name,
                email=email,
                password=make_password(password),
                role=role,
                phone=phone,
                avatar="default-avatar.png",
                is_active=True
            )
            
            return JsonResponse({
                "success": True,
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role
                }
            }, status=201)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def api_get_messages(request):
    if request.method == "GET":
        try:
            user_id = request.GET.get('user_id')
            other_id = request.GET.get('other_id')
            
            if not user_id or not other_id:
                return JsonResponse({"error": "user_id and other_id required"}, status=400)
            
            messages = Messages.objects.filter(
                sender_id__in=[user_id, other_id],
                receiver_id__in=[user_id, other_id]
            ).order_by('timestamp')
            
            messages_list = []
            for msg in messages:
                messages_list.append({
                    'id': msg.id,
                    'sender_id': msg.sender_id,
                    'receiver_id': msg.receiver_id,
                    'content': msg.content,
                    'timestamp': msg.timestamp.isoformat(),
                    'is_read': msg.is_read
                })
            
            return JsonResponse({"messages": messages_list})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Method not allowed"}, status=405)


def api_test(request):
    return JsonResponse({"message": "Django backend working"})



# Add this function to your existing views.py

def capture_video(request):
    """
    Page for capturing initial assessment video with AI analysis
    """
    return render(request, 'patient/capture-video.html')


# Add this function to your existing views.py

def physio_assessment(request):
    """
    Page for real-time physio assessment using TensorFlow.js pose detection
    """
    return render(request, 'patient/physio-assessment.html')