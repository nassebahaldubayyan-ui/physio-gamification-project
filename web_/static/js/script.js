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
    window.location.href = `/doctor/patients/${patientId}/`;
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

function goGame(gameType) {
    window.location.href = `/games/${gameType}/`;
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
// PATIENT LOGIN FUNCTION (using Django API)
// ============================================

async function loginGamer() {
    const username = document.getElementById('playerName')?.value.trim();
    const password = document.getElementById('password')?.value.trim();
    
    if (!username || !password) {
        showNotification('Please enter both username and password', 'error');
        return;
    }

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    try {
        const response = await fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (data.success && data.user_type === 'patient') {
            // Store user data
            localStorage.setItem('userId', data.user_id);
            localStorage.setItem('userType', data.user_type);
            localStorage.setItem('username', data.username);
            localStorage.setItem('firstName', data.first_name);
            localStorage.setItem('lastName', data.last_name);
            
            showNotification('Login successful!', 'success');
            setTimeout(() => window.location.href = '/patient/', 1000);
        } else {
            showNotification(data.error || 'Invalid credentials', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showNotification('Connection error. Please try again.', 'error');
    }
}

// ============================================
// DOCTOR LOGIN FUNCTION (using Django API)
// ============================================

async function loginDoctor() {
    const username = document.getElementById('doctorEmail')?.value.trim();
    const password = document.getElementById('password')?.value.trim();
    
    if (!username || !password) {
        showNotification('Please enter both email and password', 'error');
        return;
    }

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    try {
        const response = await fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (data.success && data.user_type === 'doctor') {
            // Store user data
            localStorage.setItem('userId', data.user_id);
            localStorage.setItem('userType', data.user_type);
            localStorage.setItem('username', data.username);
            localStorage.setItem('firstName', data.first_name);
            localStorage.setItem('lastName', data.last_name);
            
            showNotification('Login successful!', 'success');
            setTimeout(() => window.location.href = '/doctor/', 1000);
        } else {
            showNotification(data.error || 'Invalid credentials', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showNotification('Connection error. Please try again.', 'error');
    }
}

// ============================================
// LOGOUT FUNCTION (using Django API)
// ============================================

async function logout() {
    if (!confirm('Are you sure you want to log out?')) return;

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    try {
        await fetch('/api/logout/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            }
        });
    } catch (error) {
        console.error('Logout error:', error);
    } finally {
        // Clear localStorage
        localStorage.clear();
        sessionStorage.clear();
        window.location.href = '/';
    }
}

// ============================================
// MESSAGING SYSTEM (using Django API)
// ============================================

async function sendPatientMessage(patientId, message) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    try {
        const response = await fetch('/api/send-message/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                patient_id: patientId,
                message: message,
                sender_type: 'patient'
            })
        });

        const data = await response.json();
        
        if (data.success) {
            showNotification('Message sent!', 'success');
            return true;
        } else {
            showNotification('Failed to send message', 'error');
            return false;
        }
    } catch (error) {
        console.error('Error sending message:', error);
        showNotification('Connection error', 'error');
        return false;
    }
}

async function sendDoctorReply(patientId, message) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    try {
        const response = await fetch('/api/send-message/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                patient_id: patientId,
                message: message,
                sender_type: 'doctor'
            })
        });

        const data = await response.json();
        
        if (data.success) {
            showNotification('Reply sent!', 'success');
            return true;
        } else {
            showNotification('Failed to send reply', 'error');
            return false;
        }
    } catch (error) {
        console.error('Error sending reply:', error);
        showNotification('Connection error', 'error');
        return false;
    }
}

async function loadMessages(patientId = null) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    let url = '/api/get-messages/';
    if (patientId) {
        url += `?patient_id=${patientId}`;
    }

    try {
        const response = await fetch(url, {
            headers: {
                'X-CSRFToken': csrfToken
            }
        });

        const data = await response.json();
        
        if (data.success) {
            return data.messages;
        } else {
            showNotification('Failed to load messages', 'error');
            return [];
        }
    } catch (error) {
        console.error('Error loading messages:', error);
        showNotification('Connection error', 'error');
        return [];
    }
}

// ============================================
// NOTIFICATION SYSTEM
// ============================================

function showNotification(message, type = 'info') {
    // Remove existing notification
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();

    const notification = document.createElement('div');
    notification.className = 'notification';
    
    const colors = {
        info: 'linear-gradient(135deg, #3b82f6, #1d4ed8)',
        success: 'linear-gradient(135deg, #10b981, #059669)',
        warning: 'linear-gradient(135deg, #f59e0b, #d97706)',
        error: 'linear-gradient(135deg, #ef4444, #dc2626)'
    };
    
    const icons = {
        info: 'fa-info-circle',
        success: 'fa-check-circle',
        warning: 'fa-exclamation-triangle',
        error: 'fa-exclamation-circle'
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
        z-index: 10000;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        animation: slideIn 0.3s ease;
        display: flex;
        align-items: center;
        gap: 10px;
    `;
    
    notification.innerHTML = `<i class="fas ${icons[type]}"></i> ${message}`;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// ============================================
// SETTINGS MANAGEMENT (with Django API)
// ============================================

async function loadSettings() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    try {
        const response = await fetch('/api/get-settings/', {
            headers: {
                'X-CSRFToken': csrfToken
            }
        });

        const data = await response.json();
        
        if (data.success) {
            return data.settings;
        }
    } catch (error) {
        console.error('Error loading settings:', error);
    }

    // Fallback to localStorage
    return JSON.parse(localStorage.getItem('userSettings')) || {
        emailNotifications: true,
        smsNotifications: false,
        language: 'en',
        darkMode: false,
        largeText: false,
        animations: true,
        twoFactor: false,
        sessionTimeout: true
    };
}

async function saveSettings(settings) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    try {
        const response = await fetch('/api/save-settings/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(settings)
        });

        const data = await response.json();
        
        if (data.success) {
            localStorage.setItem('userSettings', JSON.stringify(settings));
            showNotification('Settings saved successfully!', 'success');
            return true;
        } else {
            showNotification('Failed to save settings', 'error');
            return false;
        }
    } catch (error) {
        console.error('Error saving settings:', error);
        showNotification('Connection error', 'error');
        return false;
    }
}

// ============================================
// DATE FORMATTING
// ============================================

function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

function formatTime(dateString) {
    const date = new Date(dateString);
    const options = { hour: '2-digit', minute: '2-digit' };
    return date.toLocaleTimeString('en-US', options);
}

function formatDateTime(dateString) {
    return `${formatDate(dateString)} at ${formatTime(dateString)}`;
}

function timeAgo(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const seconds = Math.floor((now - date) / 1000);
    
    const intervals = {
        year: 31536000,
        month: 2592000,
        week: 604800,
        day: 86400,
        hour: 3600,
        minute: 60
    };
    
    for (const [unit, secondsInUnit] of Object.entries(intervals)) {
        const interval = Math.floor(seconds / secondsInUnit);
        if (interval >= 1) {
            return `${interval} ${unit}${interval === 1 ? '' : 's'} ago`;
        }
    }
    
    return 'just now';
}

// ============================================
// CHECK AUTH STATUS
// ============================================

async function checkAuth() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    try {
        const response = await fetch('/api/user/', {
            headers: {
                'X-CSRFToken': csrfToken
            }
        });

        if (response.ok) {
            const data = await response.json();
            return {
                authenticated: true,
                user: data
            };
        }
    } catch (error) {
        console.error('Auth check error:', error);
    }

    return {
        authenticated: false,
        user: null
    };
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
            
            .notification {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .fa-spin {
                animation: spin 1s linear infinite;
            }
        `;
        document.head.appendChild(style);
    }
})();

// ============================================
// INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Auto-redirect if logged in
    const currentPath = window.location.pathname;
    const loginPages = ['/gamer-login/', '/doctor-login/'];
    
    if (loginPages.includes(currentPath)) {
        checkAuth().then(auth => {
            if (auth.authenticated) {
                if (auth.user.user_type === 'patient') {
                    window.location.href = '/patient/';
                } else if (auth.user.user_type === 'doctor') {
                    window.location.href = '/doctor/';
                }
            }
        });
    }
});