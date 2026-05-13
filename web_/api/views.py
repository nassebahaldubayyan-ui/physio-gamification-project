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
    print("🔥 capture_video VIEW HIT")

    # 1. Get user from session (NOT request.user)
    user_id = request.session.get("user_id")

    print("SESSION USER ID:", user_id)

    affected_hand = None

    if user_id:
        # 2. Get patient linked to this user
        patient = Patients.objects.filter(user_id=user_id).first()

        if patient:
            affected_hand = patient.affected_hand
            print("FOUND PATIENT:", patient.id)
            print("AFFECTED HAND:", affected_hand)
        else:
            print("❌ No patient found for user_id:", user_id)
    else:
        print("❌ No user_id in session")

    # 3. Default fallback (important for JS safety)
    if not affected_hand:
        affected_hand = "right"

    return render(request, "patient/capture-video.html", {
        "affected_hand": affected_hand,
        "patient_id": user_id
    })
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
    print(f"\n{'='*50}")
    print(f"🎮 game_catching_stars CALLED")
    
    user_id = request.GET.get('user_id', '').strip()
    
    if not user_id or not user_id.isdigit():
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('/gamer-login/')
    
    user_id = int(user_id)
    request.session['user_id'] = user_id
    request.session.modified = True
    
    print(f"✅ Final user_id: {user_id}")

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
    
    # تحديد المستوى
    from .models import GameSessions
    force_level = request.GET.get('force_level', '').strip()

    if force_level and force_level.isdigit():
        current_level = int(force_level)
        current_level = max(1, min(3, current_level))
        print(f"🔁 force_level used: {current_level} (PLAY AGAIN)")
    else:
        last_session = GameSessions.objects.filter(
            patient=patient,
            game_type='catching-stars'
        ).order_by('-session_date').first()
    
        if last_session is None:
            current_level = get_level_from_assessment(patient)
            print("📊 No previous sessions, starting at level 1")
        else:
            # thresholds للنجوم: 10 نقاط للمستوى 2، 20 نقطة للمستوى 3
            level_thresholds = {1: 10, 2: 20, 3: 999}
            last_level = last_session.level
            last_score = last_session.score
        
            print(f"📊 Last session - Level: {last_level}, Score: {last_score}")
        
            if last_level >= 3:
                current_level = 3
            elif last_score >= level_thresholds.get(last_level, 5):
                current_level = last_level + 1
            else:
                current_level = last_level
    
    print(f"✅ Final level: {current_level}")
    
    # قراءة ملف index.html
    file_path = os.path.join('static', 'Star_build', 'index.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # استبدال المتغيرات
    html_content = html_content.replace('__USER_ID__', str(user_id))
    html_content = html_content.replace('"__USER_ID__"', str(user_id))
    html_content = html_content.replace('__PATIENT_NAME__', patient_name)
    html_content = html_content.replace('__LEVEL__', str(current_level))
    
    # إضافة سكريبت تأكيد
    backup_script = f"""
    <script>
        window.DJANGO_USER_ID = {user_id};
        window.DJANGO_PATIENT_NAME = "{patient_name}";
        window.DJANGO_LEVEL = {current_level};
        console.log("✅ Django Backup - UserID:", window.DJANGO_USER_ID, 
                    "Patient:", window.DJANGO_PATIENT_NAME, 
                    "Level:", window.DJANGO_LEVEL);
    </script>
    """
    
    html_content = html_content.replace('</body>', backup_script + '\n</body>')
    
    print(f"{'='*50}\n")
    return HttpResponse(html_content)


def get_level_from_assessment(patient):
    """
    تحديد المستوى بناءً على التقييم الأولي
    يستخدم أقل مستوى من (الكتف، المرفق، القبضة)
    """
    shoulder = patient.shoulder_strength or 0
    elbow = patient.elbow_strength or 0
    grip = patient.grip_strength or 0
    shoulder_external = patient.shoulder_external_strength or 0

    
    print(f"📊 Assessment Values - Shoulder: {shoulder}, Elbow: {elbow}, Grip: {grip}, Shoulder_external: {shoulder_external}")
    
    # مستوى الكتف
    if shoulder <= 35:
        shoulder_level = 1
    elif shoulder <= 50:
        shoulder_level = 2
    else:
        shoulder_level = 3
    
    # مستوى المرفق
    if elbow <= 150:
        elbow_level = 1
    elif elbow <= 90:
        elbow_level = 2
    else:
        elbow_level = 3
    
    # مستوى القبضة
    if grip <= 35:
        grip_level = 1
    elif grip <= 55:
        grip_level = 2
    else:
        grip_level = 3
        
    if shoulder_external <= 55:
        shoulder_external_level = 1
    elif shoulder_external <= 70:
        shoulder_external_level = 2
    else:
        shoulder_external_level = 3
    
    print(f"📊 Levels - Shoulder: {shoulder_level}, Elbow: {elbow_level}, Grip: {grip_level}, Shoulder_external: {shoulder_external_level}")
    
    # المستوى النهائي = أقل مستوى
    current_level = min(shoulder_level, elbow_level, grip_level, shoulder_external_level)
    
    print(f"✅ Final Level from Assessment: {current_level}")
    
    return current_level

    
def game_catching_objects(request):
    print(f"\n{'='*50}")
    print(f"🎮 game_catching_objects CALLED")
    print(f"📥 GET params: {request.GET}")
    print(f"📥 Session: {dict(request.session)}")
    
    user_id = request.GET.get('user_id', '').strip()
    print(f"📥 user_id from GET: '{user_id}'")
    
    # إذا ما في user_id في GET، جرب من session
    if not user_id or not user_id.isdigit():
        user_id = request.session.get('user_id')
        print(f"📥 user_id from session: '{user_id}'")
        
        if not user_id:
            print("❌ No user_id found anywhere!")
            return redirect('/gamer-login/')
    
    user_id = int(user_id)
    request.session['user_id'] = user_id
    request.session.modified = True  # ✅ مهم: حفظ session
    
    print(f"✅ Final user_id: {user_id}")

    try:
        user = Users.objects.get(id=user_id)
        print(f"✅ User found: {user.name} (role: {user.role})")
        
        if user.role != 'patient':
            print(f"❌ User is not patient, role: {user.role}")
            return redirect('/gamer-login/')
        
        patient = Patients.objects.filter(user=user).first()
        if not patient:
            print("❌ No patient record")
            return HttpResponse("Your account is not linked to a patient record.", status=403)
        
        patient_name = user.name
        
    except Users.DoesNotExist:
        print(f"❌ User {user_id} not found")
        return redirect('/gamer-login/')
    
    # تحديد المستوى من DB
    from .models import GameSessions
    force_level = request.GET.get('force_level', '').strip()

    if force_level and force_level.isdigit():
        # المريض ضغط PLAY AGAIN — نبقى بنفس المستوى بدون ما نرفعه
        current_level = int(force_level)
        current_level = max(1, min(3, current_level))
        print(f"🔁 force_level used: {current_level} (PLAY AGAIN)")
    else:
        last_session = GameSessions.objects.filter(
            patient=patient,
            game_type='catching-objects'
        ).order_by('-session_date').first()
    
        if last_session is None:
            current_level = get_level_from_assessment(patient)
            print("📊 No previous sessions, starting at level 1")
        else:
            level_thresholds = {1: 20, 2: 40, 3: 999}
            last_level = last_session.level
            last_score = last_session.score
        
            print(f"📊 Last session - Level: {last_level}, Score: {last_score}")
        
            if last_level >= 3:
                current_level = 3
            elif last_score >= level_thresholds.get(last_level, 5):
                current_level = last_level + 1
            else:
                current_level = last_level
    
    print(f"✅ Final level: {current_level}")
    
    # ✅ قراءة الملف
    file_path = os.path.join('static', 'apple_build', 'index.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # ✅ طباعة قبل الاستبدال للتحقق
    print(f"📝 Before replace - contains __USER_ID__: {'__USER_ID__' in html_content}")
    print(f"📝 Before replace - contains __PATIENT_NAME__: {'__PATIENT_NAME__' in html_content}")
    print(f"📝 Before replace - contains __LEVEL__: {'__LEVEL__' in html_content}")
    
    # ✅ استبدال المتغيرات
    html_content = html_content.replace('__USER_ID__', str(user_id))
    html_content = html_content.replace('"__USER_ID__"', str(user_id))
    html_content = html_content.replace('__PATIENT_NAME__', patient_name)
    html_content = html_content.replace('__LEVEL__', str(current_level))
    
    # ✅ طباعة بعد الاستبدال للتحقق
    print(f"📝 After replace - contains __USER_ID__: {'__USER_ID__' in html_content}")
    print(f"📝 Final check - user {user_id} in HTML: {str(user_id) in html_content}")
    
    # ✅ إضافة سكريبت تأكيد (خطة B)
    backup_script = f"""
    <script>
        // ✅ Django Backup - يضمن إن userId موجود
        window.DJANGO_USER_ID = {user_id};
        window.DJANGO_PATIENT_NAME = "{patient_name}";
        window.DJANGO_LEVEL = {current_level};
        console.log("✅ Django Backup - UserID:", window.DJANGO_USER_ID, 
                    "Patient:", window.DJANGO_PATIENT_NAME, 
                    "Level:", window.DJANGO_LEVEL);
    </script>
    """
    
    # حقن السكريبت قبل </body>
    html_content = html_content.replace('</body>', backup_script + '\n</body>')
    
    print(f"{'='*50}\n")
    
    return HttpResponse(html_content)
    


def game_matching(request):
    
    user_id = request.GET.get('user_id', '').strip()
    
    if not user_id or not user_id.isdigit():
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('/gamer-login/')
    
    user_id = int(user_id)
    request.session['user_id'] = user_id
    request.session.modified = True

    # تحديد المستوى
    force_level = request.GET.get('force_level', '').strip()
    if force_level and force_level.isdigit():
        current_level = max(1, min(3, int(force_level)))
    else:
        current_level = 1

    try:
        user = Users.objects.get(id=user_id)
        
        if user.role != 'patient':
            return redirect('/gamer-login/')
        
        patient = Patients.objects.filter(user=user).first()
        if not patient:
            return HttpResponse("Your account is not linked to a patient record.", status=403)
        
        patient_name = user.name
        side = patient.affected_hand if patient.affected_hand else 'right'
        
    except Users.DoesNotExist:
        return redirect('/gamer-login/')
    
    file_path = os.path.join('static', 'matching_build', 'index.html')
    if not os.path.exists(file_path):
        file_path = os.path.join(settings.BASE_DIR, 'static', 'matching_build', 'index.html')
    if not os.path.exists(file_path):
        return HttpResponse("Matching game not found.", status=404)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    html_content = html_content.replace('__USER_ID__', str(user_id))
    html_content = html_content.replace('"__USER_ID__"', str(user_id))
    html_content = html_content.replace('__PATIENT_NAME__', patient_name)
    html_content = html_content.replace('__SIDE__', side)
    html_content = html_content.replace('__LEVEL__', str(current_level))
    
    backup_script = f"""
    <script>
        window.DJANGO_USER_ID = {user_id};
        window.DJANGO_PATIENT_NAME = "{patient_name}";
        window.DJANGO_LEVEL = {current_level};
        console.log("✅ Django Backup - UserID:", window.DJANGO_USER_ID,
                    "Patient:", window.DJANGO_PATIENT_NAME,
                    "Level:", window.DJANGO_LEVEL);
    </script>
    """
    html_content = html_content.replace('</body>', backup_script + '\n</body>')
    
    print(f"🎮 Matching Game - User: {user_id}, Name: {patient_name}, Level: {current_level}")
    
    return HttpResponse(html_content)

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


import json
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def api_save_game_result(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            user_id = data.get('user_id')
            if not user_id:
                return JsonResponse({"success": False, "error": "No user_id"}, status=401)

            from .models import Patients, GameSessions, Users

            try:
                user = Users.objects.get(id=user_id)
                patient = Patients.objects.filter(user=user).first()

                if not patient:
                    return JsonResponse({
                        "success": False,
                        "error": "User is not linked to patient"
                    }, status=403)

                # ======================================================
                # توحيد أسماء الألعاب
                # ======================================================
                game_type_raw = data.get('game', '')

                game_type_map = {
                    "catching_stars": "catching-stars",
                    "catching_objects": "catching-objects",
                    "matching_game": "matching-game",
                    "catching-stars": "catching-stars",
                    "catching-objects": "catching-objects",
                    "matching-game": "matching-game"
                }

                game_type = game_type_map.get(game_type_raw, game_type_raw)

                # ======================================================
                # بيانات عامة
                # ======================================================
                score = int(data.get('score', 0))
                level = int(data.get('level', 1))
                avg_elbow = data.get('avg_elbow', 0)

                # ======================================================
                # توحيد accuracy + objects حسب اللعبة
                # ======================================================
                accuracy = 0
                objects_caught = score

                if game_type == "catching-stars":
                    accuracy = data.get('grip_accuracy', 0)
                    objects_caught = data.get('stars_caught', score)

                elif game_type == "catching-objects":
                    accuracy = data.get('hand_stability', data.get('accuracy', 0))
                    objects_caught = data.get('objects_caught', score)

                elif game_type == "matching-game":
                    accuracy = data.get('accuracy', 0)
                    objects_caught = data.get('matches_made', score)

                # ======================================================
                # الحفظ في قاعدة البيانات
                # ======================================================
                GameSessions.objects.create(
                    patient=patient,
                    game_type=game_type,
                    level=level,
                    player_name=patient.user.name,
                    user_id=patient.user.id,
                    score=score,
                    duration=60,
                    accuracy=accuracy,
                    stars_caught=data.get('stars_caught', 0),
                    matches_made=data.get('matches_made', 0),
                    objects_caught=objects_caught,
                    shoulder_activation=0,
                    elbow_activation=0,
                    wrist_activation=0,
                    grip_activation=0,
                    external_rotation=0,
                    shoulder_shrug=0,
                    completed=1,
                    session_date=timezone.now()
                )

                print(f"✅ SAVED | user:{user_id} | game:{game_type} | level:{level} | score:{score}")

                return JsonResponse({
                    "success": True,
                    "message": "Saved successfully"
                })

            except Users.DoesNotExist:
                return JsonResponse({"success": False, "error": "User not found"}, status=404)

        except Exception as e:
            import traceback
            print("🔥 API ERROR:", str(e))
            print(traceback.format_exc())

            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def api_get_user_name(request):
    user_id = request.GET.get('user_id')
    user = Users.objects.get(id=user_id)
    return JsonResponse({"name": user.name})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Patients
import json
from django.utils import timezone


@csrf_exempt
def api_save_initial_assessment(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        data = json.loads(request.body)

        user_id = data.get("user_id")

        patient = Patients.objects.get(user__id=user_id)
        print("USER ID RECEIVED:", user_id)
        print("PATIENT FOUND:", patient)
        # UPDATE EXISTING PATIENT
        patient.shoulder_strength = data.get("shoulder_strength", 0)
        patient.elbow_strength = data.get("elbow_strength", 0)
        patient.grip_strength = data.get("grip_strength", 0)

        # optional tracking fields
        patient.has_assessment_video = 1
        patient.assessment_date = str(timezone.now())

        patient.save()

        return JsonResponse({
            "success": True,
            "message": "Assessment saved successfully"
        })

    except Patients.DoesNotExist:
        return JsonResponse({
            "success": False,
            "error": "Patient not found"
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        })