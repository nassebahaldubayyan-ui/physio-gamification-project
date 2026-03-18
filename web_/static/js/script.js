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
// HELPER FUNCTIONS
// ============================================

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// ============================================
// PATIENT LOGIN FUNCTION 
// ============================================

async function loginGamer() {
    const emailInput = document.getElementById('patientEmail')
    const passwordInput = document.getElementById('patientPassword') 
    
    const email = emailInput?.value.trim();
    const password = passwordInput?.value.trim();
    
    if (!email || !password) {
        showNotification('Please enter both email and password', 'error');
        return;
    }
    
    if (!validateEmail(email)) {
        showNotification('Please enter a valid email address', 'error');
        return;
    }
    
    const loadingEl = document.getElementById('loading');
    const errorEl = document.getElementById('errorMessage');
    
    if (loadingEl) loadingEl.style.display = 'block';
    if (errorEl) errorEl.style.display = 'none';
    
    try {
        const response = await fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            if (data.user.role === 'patient') {
                localStorage.setItem('userType', 'patient');
                localStorage.setItem('patientId', data.user.id);
                localStorage.setItem('patientName', data.user.name);
                localStorage.setItem('patientEmail', data.user.email);
                localStorage.setItem('patientPhone', data.user.phone || '');
                localStorage.setItem('patientAvatar', data.user.avatar || 'default-avatar.png');
                
                showNotification('Login successful! Redirecting...', 'success');
                
                setTimeout(() => {
                    window.location.href = '/patient/';
                }, 1000);
            } else {
                showNotification('This account is not a patient account', 'error');
                if (loadingEl) loadingEl.style.display = 'none';
            }
        } else {
            showNotification(data.error || 'Invalid email or password', 'error');
            if (loadingEl) loadingEl.style.display = 'none';
        }
    } catch (error) {
        console.error('Login error:', error);
        showNotification('Connection error. Please try again.', 'error');
        if (loadingEl) loadingEl.style.display = 'none';
    }
}

// ============================================
// DOCTOR LOGIN FUNCTION
// ============================================

async function loginDoctor() {
    const email = document.getElementById('doctorEmail')?.value.trim();
    const password = document.getElementById('doctorPassword')?.value.trim(); 
    
    if (!email || !password) {
        showNotification('Please enter both email and password', 'error');
        return;
    }
    
    
    const loadingEl = document.getElementById('loading');
    const errorEl = document.getElementById('errorMessage');
    
    if (loadingEl) loadingEl.style.display = 'block';
    if (errorEl) errorEl.style.display = 'none';
    
    try {
        const response = await fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            if (data.user.role === 'doctor') {
                localStorage.setItem('userType', 'doctor');
                localStorage.setItem('doctorId', data.user.id);
                localStorage.setItem('doctorName', data.user.name);
                localStorage.setItem('doctorEmail', data.user.email);
                localStorage.setItem('doctorPhone', data.user.phone || '');
                localStorage.setItem('doctorAvatar', data.user.avatar || 'default-avatar.png');
                
                showNotification('Login successful! Redirecting...', 'success');
                
                setTimeout(() => {
                    window.location.href = '/doctor/';
                }, 1000);
            } else {
                showNotification('This account is not a doctor account', 'error');
                if (loadingEl) loadingEl.style.display = 'none';
            }
        } else {
            showNotification(data.error || 'Invalid email or password', 'error');
            if (loadingEl) loadingEl.style.display = 'none';
        }
    } catch (error) {
        console.error('Login error:', error);
        showNotification('Connection error. Please try again.', 'error');
        if (loadingEl) loadingEl.style.display = 'none';
    }
}

// ============================================
// REGISTRATION FUNCTION
// ============================================

async function registerUser() {
    const name = document.getElementById('registerName')?.value.trim();
    const email = document.getElementById('registerEmail')?.value.trim();
    const password = document.getElementById('registerPassword')?.value.trim();
    const role = document.getElementById('registerRole')?.value || 'patient';
    const phone = document.getElementById('registerPhone')?.value.trim() || '';
    
    if (!name || !email || !password) {
        showNotification('Please fill in all required fields', 'error');
        return;
    }
    
    if (!validateEmail(email)) {
        showNotification('Please enter a valid email address', 'error');
        return;
    }
    
    if (password.length < 6) {
        showNotification('Password must be at least 6 characters', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                name: name,
                email: email,
                password: password,
                role: role,
                phone: phone
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Registration successful! Please login.', 'success');
            
            setTimeout(() => {
                if (role === 'doctor') {
                    window.location.href = '/doctor-login/';
                } else {
                    window.location.href = '/gamer-login/';
                }
            }, 1500);
        } else {
            showNotification(data.error || 'Registration failed', 'error');
        }
    } catch (error) {
        console.error('Registration error:', error);
        showNotification('Connection error. Please try again.', 'error');
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
        localStorage.removeItem('doctorPhone');
        localStorage.removeItem('doctorAvatar');
        
        showNotification('Logged out successfully', 'info');
        
        setTimeout(() => {
            window.location.href = '/';
        }, 1000);
    }
}

function logoutPatient() {
    if (confirm('Are you sure you want to log out?')) {
        localStorage.removeItem('userType');
        localStorage.removeItem('patientId');
        localStorage.removeItem('patientName');
        localStorage.removeItem('patientEmail');
        localStorage.removeItem('patientPhone');
        localStorage.removeItem('patientAvatar');
        
        showNotification('Logged out successfully', 'info');
        
        setTimeout(() => {
            window.location.href = '/';
        }, 1000);
    }
}

function logout() {
    if (confirm('Are you sure you want to log out?')) {
        localStorage.clear();
        
        showNotification('Logged out successfully', 'info');
        
        setTimeout(() => {
            window.location.href = '/';
        }, 1000);
    }
}

// ============================================
// NOTIFICATION SYSTEM
// ============================================

function showNotification(message, type = 'info') {
    const oldNotification = document.querySelector('.custom-notification');
    if (oldNotification) {
        oldNotification.remove();
    }
    
    const notification = document.createElement('div');
    notification.className = 'custom-notification';
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
        z-index: 9999;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        animation: slideIn 0.3s ease;
        max-width: 300px;
        text-align: center;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        }
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

function toggleDarkMode(enabled) {
    if (enabled) {
        document.body.classList.add('dark-mode');
        document.body.style.background = 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)';
    } else {
        document.body.classList.remove('dark-mode');
        document.body.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
    }
}

// ============================================
// CHECK AUTHENTICATION
// ============================================

function checkAuth(requiredType = null) {
    const userType = localStorage.getItem('userType');
    
    if (!userType) {
        return false;
    }
    
    if (requiredType && userType !== requiredType) {
        return false;
    }
    
    return true;
}

function requireAuth(requiredType = null, redirectUrl = '/') {
    if (!checkAuth(requiredType)) {
        showNotification('Please login first', 'warning');
        window.location.href = redirectUrl;
        return false;
    }
    return true;
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
    return `${formatDate(date)} at ${formatTime(date)}`;
}

// ============================================
// ADD ANIMATION STYLES
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
            
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            
            .dark-mode {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            }
            
            .dark-mode .login-container,
            .dark-mode .welcome-container,
            .dark-mode .edit-container,
            .dark-mode .settings-container {
                background: rgba(30, 30, 46, 0.95);
                color: #fff;
            }
        `;
        document.head.appendChild(style);
    }
})();

// ============================================
// ASSESSMENT VIDEO FUNCTIONS
// ============================================
function checkAssessmentStatus() {
    const hasVideo = localStorage.getItem('hasAssessmentVideo') === 'true';
    const assessmentDate = localStorage.getItem('assessmentDate') || 'Never';
    const assessmentBadge = document.getElementById('assessmentBadge');
    const assessmentStatus = document.getElementById('assessmentStatus');
    const assessmentDateEl = document.getElementById('assessmentDate');
    
    if (hasVideo) {
        assessmentBadge.textContent = 'Completed';
        assessmentBadge.className = 'status-badge completed';
        assessmentDateEl.textContent = assessmentDate;
    } else {
        assessmentBadge.textContent = 'Not Completed';
        assessmentBadge.className = 'status-badge pending';
        assessmentDateEl.textContent = 'Never';
    }
}

function goToAssessment() {
    window.location.href = "{% url 'capture_video' %}";
}

// ============================================
// INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            this.value = this.value.replace(/[^0-9+]/g, '');
        });
    });
    
    const currentPath = window.location.pathname;
    const protectedPaths = ['/patient/', '/doctor/', '/profile/', '/settings/'];
    
    if (protectedPaths.some(path => currentPath.startsWith(path))) {
        const userType = localStorage.getItem('userType');
        
        if (!userType) {
            showNotification('Please login first', 'warning');
            setTimeout(() => {
                window.location.href = '/';
            }, 1500);
        }
        
        if (currentPath.startsWith('/doctor/') && userType !== 'doctor') {
            showNotification('Access denied. Doctor only.', 'error');
            setTimeout(() => {
                window.location.href = '/';
            }, 1500);
        }
        
        if (currentPath.startsWith('/patient/') && userType !== 'patient') {
            showNotification('Access denied. Patient only.', 'error');
            setTimeout(() => {
                window.location.href = '/';
            }, 1500);
        }
    }
});