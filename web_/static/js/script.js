// ============================================
// MAIN NAVIGATION FUNCTIONS
// ============================================

function goHome() {
    window.location.href = "/";
}

function goDoctor() {
    window.location.href = "/doctor/";
}

function goPatient() {
    window.location.href = "/patient/";
}

function goGamerLogin() {
    window.location.href = "/gamer-login/";
}

function goDoctorLogin() {
    window.location.href = "/doctor-login/";
}

// ============================================
// DOCTOR NAVIGATION FUNCTIONS
// ============================================

function goPatients() {
    window.location.href = "/doctor/patients/";
}

function goPatientDetails(patientId) {
    window.location.href = `/doctor/patient-details/?patient=${patientId}`;
}

function goDoctorMessages() {
    window.location.href = "/doctor/messages/";
}

function goPerformance() {
    window.location.href = "/doctor/performance/";
}

function goDoctorProfile() {
    window.location.href = "/profile/";
}

function goDoctorSettings() {
    window.location.href = "/settings/";
}

// ============================================
// PATIENT NAVIGATION FUNCTIONS
// ============================================

function goGame(gameNumber) {
    if (gameNumber === 1) window.location.href = "/games/catching-stars/";
    else if (gameNumber === 2) window.location.href = "/games/matching/";
    else if (gameNumber === 3) window.location.href = "/games/catching-objects/";
}

function goResult() {
    window.location.href = "/patient/result/";
}

function goChat() {
    window.location.href = "/patient/chat/";
}

function goPatientProfile() {
    window.location.href = "/profile/";
}

function goPatientSettings() {
    window.location.href = "/settings/";
}

// ============================================
// PATIENT LOGIN FUNCTION
// ============================================

function loginGamer() {
    const name = document.getElementById('playerName')?.value.trim();
    const id = document.getElementById('playerId')?.value.trim();
    
    if (!name || !id) {
        alert('Please enter both name and player ID');
        return;
    }
    
    // Valid patients database (simulated)
    const validPlayers = {
        'PT001': { name: 'Ali', level: 4, condition: 'Motor Disability' },
        'PT002': { name: 'Sara', level: 3, condition: 'Arm Weakness' },
        'PT003': { name: 'Omar', level: 5, condition: 'Movement Disorder' }
    };
    
    if (validPlayers[id]) {
        localStorage.setItem('patientName', validPlayers[id].name);
        localStorage.setItem('patientId', id);
        localStorage.setItem('patientLevel', validPlayers[id].level);
        localStorage.setItem('patientCondition', validPlayers[id].condition);
        localStorage.setItem('userType', 'patient');
        window.location.href = '/patient/';
    } else {
        alert('Invalid Player ID. Please check and try again.');
    }
}

// ============================================
// DOCTOR LOGIN FUNCTION
// ============================================

function loginDoctor() {
    const email = document.getElementById('doctorEmail')?.value.trim();
    const id = document.getElementById('doctorId')?.value.trim();
    
    if (!email || !id) {
        alert('Please enter both email and doctor ID');
        return;
    }
    
    // Valid doctors database (simulated)
    const validDoctors = {
        'TH001': { 
            name: 'Dr. Ahmad', 
            email: 'dr.ahmad@clinic.com',
            specialty: 'Physiotherapy',
            phone: '+966 50 000 0000'
        },
        'TH002': { 
            name: 'Dr. Sarah', 
            email: 'dr.sarah@clinic.com',
            specialty: 'Occupational Therapy',
            phone: '+966 50 111 1111'
        }
    };
    
    if (validDoctors[id] && validDoctors[id].email === email) {
        localStorage.setItem('userType', 'doctor');
        localStorage.setItem('doctorId', id);
        localStorage.setItem('doctorName', validDoctors[id].name);
        localStorage.setItem('doctorEmail', email);
        localStorage.setItem('doctorSpecialty', validDoctors[id].specialty);
        localStorage.setItem('doctorPhone', validDoctors[id].phone);
        window.location.href = '/doctor/';
    } else {
        alert('Invalid credentials. Please check your email and doctor ID.');
    }
}

// ============================================
// LOGOUT FUNCTIONS
// ============================================

function logoutDoctor() {
    if (confirm('Are you sure you want to log out?')) {
        localStorage.removeItem('userType');
        localStorage.removeItem('doctorId');
        localStorage.removeItem('doctorName');
        localStorage.removeItem('doctorEmail');
        localStorage.removeItem('doctorSpecialty');
        localStorage.removeItem('doctorPhone');
        window.location.href = '/';
    }
}

function logoutPatient() {
    if (confirm('Are you sure you want to log out?')) {
        localStorage.removeItem('userType');
        localStorage.removeItem('patientName');
        localStorage.removeItem('patientId');
        localStorage.removeItem('patientLevel');
        localStorage.removeItem('patientCondition');
        window.location.href = '/';
    }
}

// ============================================
// NOTIFICATION SYSTEM
// ============================================

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.textContent = message;
    
    const colors = {
        info: 'linear-gradient(135deg, #3b82f6, #1d4ed8)',
        success: 'linear-gradient(135deg, #10b981, #059669)',
        warning: 'linear-gradient(135deg, #f59e0b, #d97706)',
        error: 'linear-gradient(135deg, #ef4444, #dc2626)'
    };
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        border-radius: 8px;
        background: ${colors[type] || colors.info};
        color: white;
        font-weight: 500;
        z-index: 1000;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// ============================================
// SETTINGS MANAGEMENT
// ============================================

function loadSettings() {
    const settings = JSON.parse(localStorage.getItem('userSettings')) || {
        emailNotifications: true,
        smsNotifications: false,
        language: 'en',
        darkMode: false,
        largeText: false,
        animations: true
    };
    return settings;
}

function saveSettings(settings) {
    localStorage.setItem('userSettings', JSON.stringify(settings));
    showNotification('Settings saved successfully!', 'success');
}

// ============================================
// DATE FORMATTING
// ============================================

function formatDate(date) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(date).toLocaleDateString('en-US', options);
}

function formatTime(date) {
    const options = { hour: '2-digit', minute: '2-digit' };
    return new Date(date).toLocaleTimeString('en-US', options);
}

// Add animation styles
(function addAnimationStyles() {
    if (!document.querySelector('#animation-styles')) {
        const style = document.createElement('style');
        style.id = 'animation-styles';
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
        `;
        document.head.appendChild(style);
    }
})();