from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.shortcuts import redirect
from .models import Users, Messages, Patients, Doctors, GameSessions
import json
import os

# NOTE: send_mail is imported INSIDE the function to avoid circular imports

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
    patient = Patients.objects.first()
    level = patient.current_level or 1

    return render(request, 'patient/patient.html', {
        'level': level
    })

def patient_chat(request):
    return render(request, 'patient/patient-chat.html')

def patient_game(request):
    return render(request, 'patient/patient-game.html')

def patient_result(request):
    return render(request, 'patient/patient-result.html')

def edit_patient_profile(request):
    return render(request, 'patient/edit-patient-profile.html')

def capture_video(request):
    return render(request, 'patient/capture-video.html')

def physio_assessment(request):
    return render(request, 'patient/physio-assessment.html')

def patient_progress(request):
    return render(request, 'patient-progress.html')

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
    
    user_id = request.GET.get('user_id', '').strip()
    
    if not user_id or not user_id.isdigit():
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('/gamer-login/')
    
    user_id = int(user_id)
    
    request.session['user_id'] = user_id
    
    try:
        user = Users.objects.get(id=user_id)
        
        if user.role != 'patient':
            return redirect('/gamer-login/')
        
        patient = Patients.objects.filter(user=user).first()
        if not patient:
            return HttpResponse("Your account is not linked to a patient record.", status=403)
        
        patient_name = user.name
        
    except Users.DoesNotExist:
        return redirect('/gamer-login/')
    
    file_path = os.path.join('static', 'Star_build', 'index.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    html_content = html_content.replace('__USER_ID__', str(user_id))
    html_content = html_content.replace('"__USER_ID__"', str(user_id))
    html_content = html_content.replace('__PATIENT_NAME__', patient_name)
    html_content = html_content.replace('__LEVEL__', '1')

    html_content = html_content.replace('console.log("Logged in user:", userId, userName);', 'console.log("Logged in user:", userId);')
    print(f"sending to html  {user_id}, patient name {patient_name}" )
    return HttpResponse(html_content)
    
def game_catching_objects(request):
    user_id = request.GET.get('user_id', '').strip()
    
    if not user_id or not user_id.isdigit():
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('/gamer-login/')
    
    user_id = int(user_id)
    
    request.session['user_id'] = user_id
    
    try:
        user = Users.objects.get(id=user_id)
        
        if user.role != 'patient':
            return redirect('/gamer-login/')
        
        patient = Patients.objects.filter(user=user).first()
        if not patient:
            return HttpResponse("Your account is not linked to a patient record.", status=403)
        
        patient_name = user.name
        
    except Users.DoesNotExist:
        return redirect('/gamer-login/')
    
    file_path = os.path.join('static', 'apple_build', 'index.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    html_content = html_content.replace('__USER_ID__', str(user_id))
    html_content = html_content.replace('"__USER_ID__"', str(user_id))
    html_content = html_content.replace('__PATIENT_NAME__', patient_name)
    html_content = html_content.replace('__LEVEL__', '1')

    html_content = html_content.replace('console.log("Logged in user:", userId, userName);', 'console.log("Logged in user:", userId);')
    print(f"sending to html  {user_id}, patient name {patient_name}" )
    return HttpResponse(html_content)
    

def game_matching(request):
    return render(request, 'games/game-matching.html')

# Static Pages
def about_us(request):
    """About Us page"""
    return render(request, 'about-us.html')

def contact_us(request):
    """Contact Us page"""
    return render(request, 'contact-us.html')

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
                    request.session['user_id'] = user.id
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
@require_http_methods(["GET"])
def api_get_messages(request):
    """Get messages between two users"""
    try:
        user_id = request.GET.get('user_id')
        user_type = request.GET.get('user_type')
        other_id = request.GET.get('other_id')
        other_type = request.GET.get('other_type')
        
        if not all([user_id, user_type, other_id, other_type]):
            return JsonResponse({"error": "All parameters required"}, status=400)
        
        messages = Messages.objects.filter(
            (
                models.Q(sender_id=user_id, sender_type=user_type, receiver_id=other_id, receiver_type=other_type) |
                models.Q(sender_id=other_id, sender_type=other_type, receiver_id=user_id, receiver_type=user_type)
            )
        ).order_by('created_at')
        
        # Mark messages as read
        Messages.objects.filter(
            sender_id=other_id,
            sender_type=other_type,
            receiver_id=user_id,
            receiver_type=user_type,
            is_read=False
        ).update(is_read=True)
        
        messages_list = []
        for msg in messages:
            messages_list.append({
                'id': msg.id,
                'sender_id': msg.sender_id,
                'sender_type': msg.sender_type,
                'receiver_id': msg.receiver_id,
                'receiver_type': msg.receiver_type,
                'content': msg.content,
                'created_at': msg.created_at,
                'is_read': msg.is_read
            })
        
        return JsonResponse({
            "success": True,
            "messages": messages_list
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def api_get_conversations(request):
    """Get all conversations for a user"""
    try:
        user_id = request.GET.get('user_id')
        user_type = request.GET.get('user_type')
        
        if not user_id or not user_type:
            return JsonResponse({"error": "user_id and user_type required"}, status=400)
        
        messages = Messages.objects.filter(
            models.Q(sender_id=user_id, sender_type=user_type) |
            models.Q(receiver_id=user_id, receiver_type=user_type)
        ).order_by('-created_at')
        
        conversations = {}
        for msg in messages:
            if str(msg.sender_id) == str(user_id) and msg.sender_type == user_type:
                partner_id = msg.receiver_id
                partner_type = msg.receiver_type
            else:
                partner_id = msg.sender_id
                partner_type = msg.sender_type
            
            key = f"{partner_type}_{partner_id}"
            
            if key not in conversations:
                try:
                    if partner_type == 'doctor':
                        user = Users.objects.get(id=partner_id)
                        partner_name = user.name
                    else:
                        user = Users.objects.get(id=partner_id)
                        partner_name = user.name
                except Users.DoesNotExist:
                    partner_name = f"{partner_type.capitalize()} {partner_id}"
                
                conversations[key] = {
                    'partner_id': partner_id,
                    'partner_type': partner_type,
                    'partner_name': partner_name,
                    'last_message': msg.content,
                    'last_message_time': msg.created_at,
                    'unread_count': 0
                }
        
        for key, conv in conversations.items():
            conv['unread_count'] = Messages.objects.filter(
                sender_id=conv['partner_id'],
                sender_type=conv['partner_type'],
                receiver_id=user_id,
                receiver_type=user_type,
                is_read=False
            ).count()
        
        return JsonResponse({
            "success": True,
            "conversations": list(conversations.values())
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_send_message(request):
    """Send a new message"""
    try:
        data = json.loads(request.body)
        
        sender_id = data.get('sender_id')
        sender_type = data.get('sender_type')
        receiver_id = data.get('receiver_id')
        receiver_type = data.get('receiver_type')
        content = data.get('content', '').strip()
        
        if not all([sender_id, sender_type, receiver_id, receiver_type, content]):
            return JsonResponse({"error": "Missing required fields"}, status=400)
        
        message = Messages.objects.create(
            sender_id=sender_id,
            sender_type=sender_type,
            receiver_id=receiver_id,
            receiver_type=receiver_type,
            content=content,
            is_read=0,
            created_at=timezone.now().isoformat()
        )
        
        return JsonResponse({
            "success": True,
            "message": {
                'id': message.id,
                'sender_id': message.sender_id,
                'sender_type': message.sender_type,
                'receiver_id': message.receiver_id,
                'receiver_type': message.receiver_type,
                'content': message.content,
                'created_at': message.created_at,
                'is_read': message.is_read
            }
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_update_assessment_status(request):
    """Update patient's assessment video status"""
    try:
        data = json.loads(request.body)
        patient_id = data.get('patient_id')
        has_video = data.get('has_video', True)
        
        if not patient_id:
            return JsonResponse({"error": "patient_id required"}, status=400)
        
        try:
            patient_profile = Patients.objects.get(user_id=patient_id)
            patient_profile.has_assessment_video = 1 if has_video else 0
            patient_profile.assessment_date = timezone.now().isoformat()
            patient_profile.save()
        except Patients.DoesNotExist:
            patient_profile = Patients.objects.create(
                user_id=patient_id,
                patient_id=f"PT{patient_id}",
                date_of_birth='',
                gender='',
                medical_condition='',
                therapy_type='',
                affected_hand='right',
                has_assessment_video=1 if has_video else 0,
                assessment_date=timezone.now().isoformat()
            )
        
        return JsonResponse({
            "success": True,
            "message": "Assessment status updated"
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def send_contact_message(request):
    """Send contact form message to email"""
    try:
        data = json.loads(request.body)
        name = data.get('name', '')
        email = data.get('email', '')
        subject = data.get('subject', 'No subject')
        message = data.get('message', '')
        
        if not name or not email or not message:
            return JsonResponse({
                'success': False,
                'error': 'Please fill in all required fields'
            }, status=400)
        
        email_subject = f"Contact Form: {subject}"
        email_body = f"""
You received a new message from PhysioPlay contact form:


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 SENDER INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name: {name}
Email: {email}
Subject: {subject}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 MESSAGE:
{message}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sent from PhysioPlay website contact form
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        
        # Import send_mail INSIDE the function to avoid circular import issues
        from django.core.mail import send_mail
        
        send_mail(
            subject=email_subject,
            message=email_body,
            from_email='physioplay.support@gmail.com',
            recipient_list=['physioplay.support@gmail.com'],
            fail_silently=False,
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Your message has been sent successfully! We will get back to you soon.'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f"Failed to send message: {str(e)}"
        }, status=500)


def api_test(request):
    return JsonResponse({"message": "Django backend working"})

def apple_game(request):
    return render(request, 'game.html')

from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def api_save_game_result(request):
    print("API called - saving game result")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            score = data.get('score', 0)
            user_id = data.get('user_id', None)
            game_type = data.get('game', 'catching_stars')
            level = data.get('level', 1)
            
            accuracy = data.get('accuracy', 0)
            avg_elbow = data.get('avg_elbow', 0)
            grip_accuracy = data.get('grip_accuracy', 0) 
            hand_stability = data.get('hand_stability', 0)  
            objects_caught = data.get('objects_caught', score)
            stars_caught = data.get('stars_caught', score)
            
            from .models import Patients, GameSessions, Users
            
            if not user_id:
                return JsonResponse({"success": False, "error": "No user_id"}, status=401)
            
            try:
                user = Users.objects.get(id=user_id)
                patient = Patients.objects.filter(user=user).first()

                if not patient:
                    print("❌ NO PATIENT FOUND FOR USER:", user_id)
                    return JsonResponse({
                        "success": False,
                        "error": "User is not linked to patient"
                    }, status=403)

                if game_type == 'catching_stars':
                    final_accuracy = grip_accuracy if grip_accuracy > 0 else accuracy
                    objects_caught_final = stars_caught
                else:
                    final_accuracy = hand_stability if hand_stability > 0 else accuracy
                    objects_caught_final = objects_caught

                GameSessions.objects.create(
                    patient=patient,
                    game_type=game_type,  
                    level=level,
                    score=score,
                    duration=60,
                    accuracy=final_accuracy,
                    objects_caught=objects_caught_final,
                    completed=1,
                    session_date=timezone.now()
                )
                print(f"✅ SAVED: user {user_id}, game {game_type}, score {score}")
                return JsonResponse({
                    "success": True,
                    "message": "Saved successfully"
                })
                
            except Users.DoesNotExist:
                return JsonResponse({"success": False, "error": "User not found"}, status=404)
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def api_get_user_name(request):
    user_id = request.GET.get('user_id')
    user = Users.objects.get(id=user_id)
    return JsonResponse({"name": user.name})