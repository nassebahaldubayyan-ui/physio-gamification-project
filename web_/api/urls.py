from django.urls import path
from . import views

urlpatterns = [
    # HTML Pages
    path('', views.index, name='index'),
    path('gamer-login/', views.gamer_login, name='gamer-login'),
    path('doctor-login/', views.doctor_login, name='doctor-login'),
    path('patient/', views.patient_dashboard, name='patient'),
    path('doctor/', views.doctor_dashboard, name='doctor'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('select-patient/', views.select_patient, name='select-patient'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    
    # Patient Pages
    path('patient-chat/', views.patient_chat, name='patient-chat'),
    path('patient-game/', views.patient_game, name='patient-game'),
    path('patient-result/', views.patient_result, name='patient-result'),
    path('patient-progress/', views.patient_progress, name='patient-progress'),
    path('edit-patient-profile/', views.edit_patient_profile, name='edit-patient-profile'),
    path('capture-video/', views.capture_video, name='capture-video'),
    path('aitest/', views.physio_assessment, name='aitest'),
    
    # Doctor Pages
    path('doctor-patients/', views.doctor_patients, name='doctor-patients'),
    path('doctor-patient-details/', views.doctor_patient_details, name='doctor-patient-details'),
    path('doctor-messages/', views.doctor_messages, name='doctor-messages'),
    path('doctor-performance/', views.doctor_performance, name='doctor-performance'),
    path('edit-doctor-profile/', views.edit_doctor_profile, name='edit-doctor-profile'),
    
    # Game Pages
    path('game-catching-stars/', views.game_catching_stars, name='game-catching-stars'),
    path('game-catching-objects/', views.game_catching_objects, name='game-catching-objects'),
    path('game-matching/', views.game_matching, name='game-matching'),
    
    # ========== API Routes ==========
    path('api/login/', views.api_login, name='api-login'),
    path('api/register/', views.api_register, name='api-register'),
    path('api/get-messages/', views.api_get_messages, name='api-get-messages'),
    path('api/send-message/', views.api_send_message, name='api-send-message'),
    path('api/test/', views.api_test, name='api-test'),
]