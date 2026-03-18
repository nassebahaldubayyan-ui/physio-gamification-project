from django.urls import path
from . import views

urlpatterns = [
    # ========== APIs ==========
    path('api/test/', views.api_test),
    path('api/login/', views.api_login),
    path('api/register/', views.api_register),
    path('api/messages/', views.api_get_messages),
    
    # ========== HTML PAGES ==========
    # Main Pages
    path('', views.index, name='index'),
    path('gamer-login/', views.gamer_login, name='gamer_login'),
    path('doctor-login/', views.doctor_login, name='doctor_login'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('select-patient/', views.select_patient, name='select_patient'),
    
    # Patient Pages
    path('patient/', views.patient_dashboard, name='patient_dashboard'),
    path('patient/chat/', views.patient_chat, name='patient_chat'),
    path('patient/game/', views.patient_game, name='patient_game'),
    path('patient/result/', views.patient_result, name='patient_result'),
    path('patient/edit/', views.edit_patient_profile, name='edit_patient_profile'),
    path('patient/capture-video/', views.capture_video, name='capture_video'),
    path('patient/physio-assessment/', views.physio_assessment, name='physio_assessment'),  # ✅ NEW PAGE
    
    # Doctor Pages
    path('doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/patients/', views.doctor_patients, name='doctor_patients'),
    path('doctor/patient-details/', views.doctor_patient_details, name='doctor_patient_details'),
    path('doctor/messages/', views.doctor_messages, name='doctor_messages'),
    path('doctor/performance/', views.doctor_performance, name='doctor_performance'),
    path('doctor/edit/', views.edit_doctor_profile, name='edit_doctor_profile'),
    
    # Game Pages
    path('games/catching-stars/', views.game_catching_stars, name='game_catching_stars'),
    path('games/catching-objects/', views.game_catching_objects, name='game_catching_objects'),
    path('games/matching/', views.game_matching, name='game_matching'),
]