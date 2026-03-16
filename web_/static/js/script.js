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
    window.location.href = "/doctor-patients/";
}

function goPatientDetails(patientId) {
    window.location.href = `/doctor-patient-details/?patient=${patientId}`;
}

function goDoctorMessages() {
    window.location.href = "/doctor-messages/";
}

function goPerformance() {
    window.location.href = "/doctor-performance/";
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
    window.location.href = `/patient-game/?game=${gameNumber}`;
}

function goResult() {
    window.location.href = "/patient-result/";
}

function goChat() {
    window.location.href = "/patient-chat/";
}

function goPatientProfile() {
    window.location.href = "/profile/";
}

function goPatientSettings() {
    window.location.href = "/settings/";
}


// ============================================
// DOCTOR LOGIN FUNCTION (SIMULATED)
// ============================================

function loginDoctor() {
    const email = document.getElementById('doctorEmail')?.value.trim();
    const id = document.getElementById('doctorId')?.value.trim();
    
    if (!email || !id) {
        showNotification('Please enter both email and doctor ID', 'error');
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
        window.location.href = '/doctor/';
    } else {
        showNotification('Invalid credentials. Please check your email and doctor ID.', 'error');
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
    return conversations[patientId];
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

function getConversations() {
    return JSON.parse(localStorage.getItem('conversations')) || {};
}

function getConversation(patientId) {
    const conversations = getConversations();
    return conversations[patientId] || null;
}

// ============================================
// NOTIFICATION SYSTEM
// ============================================

function showNotification(message, type = 'info', duration = 3000) {
    // Check if notification container exists, if not create it
    let container = document.getElementById('notification-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'notification-container';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
        `;
        document.body.appendChild(container);
    }
    
    const notification = document.createElement('div');
    notification.textContent = message;
    
    const colors = {
        info: 'linear-gradient(135deg, #3b82f6, #1d4ed8)',
        success: 'linear-gradient(135deg, #10b981, #059669)',
        warning: 'linear-gradient(135deg, #f59e0b, #d97706)',
        error: 'linear-gradient(135deg, #ef4444, #dc2626)'
    };
    
    notification.style.cssText = `
        padding: 15px 25px;
        border-radius: 8px;
        background: ${colors[type] || colors.info};
        color: white;
        font-weight: 500;
        margin-bottom: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        animation: slideIn 0.3s ease;
        cursor: pointer;
    `;
    
    notification.onclick = function() {
        this.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => this.remove(), 300);
    };
    
    container.appendChild(notification);
    
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }
    }, duration);
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
    applySettings(settings);
}

function applySettings(settings) {
    // Apply dark mode
    if (settings.darkMode) {
        document.body.classList.add('dark-mode');
    } else {
        document.body.classList.remove('dark-mode');
    }
    
    // Apply large text
    if (settings.largeText) {
        document.body.classList.add('large-text');
    } else {
        document.body.classList.remove('large-text');
    }
    
    // Apply language
    if (settings.language === 'ar') {
        document.documentElement.dir = 'rtl';
    } else {
        document.documentElement.dir = 'ltr';
    }
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

function formatDateTime(date) {
    const options = { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit', 
        minute: '2-digit' 
    };
    return new Date(date).toLocaleDateString('en-US', options);
}

// ============================================
// LOCAL STORAGE HELPERS
// ============================================

function setItem(key, value) {
    if (typeof value === 'object') {
        localStorage.setItem(key, JSON.stringify(value));
    } else {
        localStorage.setItem(key, value);
    }
}

function getItem(key, defaultValue = null) {
    const value = localStorage.getItem(key);
    if (value === null) return defaultValue;
    
    try {
        return JSON.parse(value);
    } catch {
        return value;
    }
}

function removeItem(key) {
    localStorage.removeItem(key);
}

function clearStorage() {
    localStorage.clear();
}

// ============================================
// USER TYPE CHECK
// ============================================

function isDoctor() {
    return localStorage.getItem('userType') === 'doctor';
}

function isPatient() {
    return localStorage.getItem('userType') === 'patient';
}

function getCurrentUser() {
    const userType = localStorage.getItem('userType');
    if (userType === 'doctor') {
        return {
            type: 'doctor',
            id: localStorage.getItem('doctorId'),
            name: localStorage.getItem('doctorName'),
            email: localStorage.getItem('doctorEmail'),
            specialty: localStorage.getItem('doctorSpecialty')
        };
    } else if (userType === 'patient') {
        return {
            type: 'patient',
            id: localStorage.getItem('patientId'),
            name: localStorage.getItem('patientName'),
            level: localStorage.getItem('patientLevel'),
            condition: localStorage.getItem('patientCondition')
        };
    }
    return null;
}

// ============================================
// API HELPERS (for Django backend)
// ============================================

async function apiGet(url) {
    try {
        const response = await fetch(url, {
            headers: {
                'X-CSRFToken': getCsrfToken()
            }
        });
        return await response.json();
    } catch (error) {
        console.error('API GET error:', error);
        showNotification('Connection error', 'error');
        return null;
    }
}

async function apiPost(url, data) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify(data)
        });
        return await response.json();
    } catch (error) {
        console.error('API POST error:', error);
        showNotification('Connection error', 'error');
        return null;
    }
}

function getCsrfToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue || '';
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
            
            @keyframes slideOut {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
            
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            @keyframes fadeOut {
                from { opacity: 1; }
                to { opacity: 0; }
            }
            
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            
            @keyframes spin {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
            
            .dark-mode {
                background: #1a1a2e !important;
                color: #e0e0e0 !important;
            }
            
            .large-text {
                font-size: 120% !important;
            }
            
            .loading-spinner {
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 3px solid rgba(255,255,255,.3);
                border-radius: 50%;
                border-top-color: white;
                animation: spin 1s ease-in-out infinite;
            }
        `;
        document.head.appendChild(style);
    }
})();

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Apply saved settings
    const settings = loadSettings();
    applySettings(settings);
    
    // Check if user is logged in for protected pages
    const protectedPages = ['/patient/', '/doctor/', '/profile/', '/settings/'];
    const currentPath = window.location.pathname;
    
    if (protectedPages.includes(currentPath)) {
        const user = getCurrentUser();
        if (!user) {
            window.location.href = '/';
        }
    }
});