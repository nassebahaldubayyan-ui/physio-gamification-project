// ============================================
// MAIN NAVIGATION FUNCTIONS
// ============================================

function goHome() {
    window.location.href = "index.html";
}

function goDoctor() {
    window.location.href = "doctor.html";
}

function goPatient() {
    window.location.href = "patient.html";
}

function goGamerLogin() {
    window.location.href = "gamer-login.html";
}

function goDoctorLogin() {
    window.location.href = "doctor-login.html";
}

// ============================================
// DOCTOR NAVIGATION FUNCTIONS
// ============================================

function goPatients() {
    window.location.href = "doctor-patients.html";
}

function goPatientDetails(patientId) {
    window.location.href = `doctor-patient-details.html?patient=${patientId}`;
}

function goDoctorMessages() {
    window.location.href = "doctor-messages.html";
}

function goPerformance() {
    window.location.href = "doctor-performance.html";
}

function goDoctorProfile() {
    window.location.href = "profile.html";
}

function goDoctorSettings() {
    window.location.href = "settings.html";
}

// ============================================
// PATIENT NAVIGATION FUNCTIONS
// ============================================

function goGame(gameNumber) {
    window.location.href = `patient-game.html?game=${gameNumber}`;
}

function goResult() {
    window.location.href = "patient-result.html";
}

function goChat() {
    window.location.href = "patient-chat.html";
}

function goPatientProfile() {
    window.location.href = "profile.html";
}

function goPatientSettings() {
    window.location.href = "settings.html";
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
        window.location.href = 'patient.html';
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
    
    // Verify email matches doctor ID
    if (validDoctors[id] && validDoctors[id].email === email) {
        localStorage.setItem('userType', 'doctor');
        localStorage.setItem('doctorId', id);
        localStorage.setItem('doctorName', validDoctors[id].name);
        localStorage.setItem('doctorEmail', email);
        localStorage.setItem('doctorSpecialty', validDoctors[id].specialty);
        localStorage.setItem('doctorPhone', validDoctors[id].phone);
        window.location.href = 'doctor.html';
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
        window.location.href = 'index.html';
    }
}

function logoutPatient() {
    if (confirm('Are you sure you want to log out?')) {
        localStorage.removeItem('userType');
        localStorage.removeItem('patientName');
        localStorage.removeItem('patientId');
        localStorage.removeItem('patientLevel');
        localStorage.removeItem('patientCondition');
        window.location.href = 'index.html';
    }
}

// ============================================
// MESSAGING SYSTEM
// ============================================

function sendPatientMessage(patientId, message) {
    let conversations = JSON.parse(localStorage.getItem('conversations')) || {};
    
    if (!conversations[patientId]) {
        conversations[patientId] = {
            patientName: localStorage.getItem('patientName') || 'Unknown',
            patientId: patientId,
            messages: []
        };
    }
    
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    
    conversations[patientId].messages.push({
        sender: 'patient',
        text: message,
        time: timeString
    });
    
    localStorage.setItem('conversations', JSON.stringify(conversations));
}

function sendDoctorReply(patientId, message) {
    let conversations = JSON.parse(localStorage.getItem('conversations')) || {};
    
    if (conversations[patientId]) {
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
        
        conversations[patientId].messages.push({
            sender: 'doctor',
            text: message,
            time: timeString
        });
        
        localStorage.setItem('conversations', JSON.stringify(conversations));
        return true;
    }
    return false;
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
        animations: true,
        twoFactor: false,
        sessionTimeout: true
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

// ============================================
// ANIMATION STYLES
// ============================================

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