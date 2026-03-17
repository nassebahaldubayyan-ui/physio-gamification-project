document.addEventListener('DOMContentLoaded', function () {
    const token = localStorage.getItem('token');
    const user = JSON.parse(localStorage.getItem('user') || '{}');

    if (!token || !user.id) {
        window.location.href = 'index.html';
    }

    document.getElementById('loading').style.display = 'none';

    // Check and load settings
    loadSettings();

    function loadSettings() {
        const settings = JSON.parse(localStorage.getItem('settings')) || {
            emailNotifications: true,
            smsNotifications: false,
            language: 'en',
            darkMode: false,
            largeText: false,
            animations: true,
            twoFactor: false,
            sessionTimeout: true,
            dataBackup: true
        };

        document.getElementById('emailNotifications').checked = settings.emailNotifications;
        document.getElementById('smsNotifications').checked = settings.smsNotifications;
        document.getElementById('language').value = settings.language;
        document.getElementById('darkMode').checked = settings.darkMode;
        document.getElementById('largeText').checked = settings.largeText;
        document.getElementById('animations').checked = settings.animations;
        document.getElementById('twoFactor').checked = settings.twoFactor;
        document.getElementById('sessionTimeout').checked = settings.sessionTimeout;
        document.getElementById('dataBackup').checked = settings.dataBackup;

        if (settings.darkMode) {
            document.body.style.background = 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)';
        } else {
            document.body.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        }
    }

    function saveSettings() {
        const settings = {
            emailNotifications: document.getElementById('emailNotifications').checked,
            smsNotifications: document.getElementById('smsNotifications').checked,
            language: document.getElementById('language').value,
            darkMode: document.getElementById('darkMode').checked,
            largeText: document.getElementById('largeText').checked,
            animations: document.getElementById('animations').checked,
            twoFactor: document.getElementById('twoFactor').checked,
            sessionTimeout: document.getElementById('sessionTimeout').checked,
            dataBackup: document.getElementById('dataBackup').checked
        };

        localStorage.setItem('settings', JSON.stringify(settings));
        showNotification('Settings saved successfully!', 'success');

        if (settings.darkMode) {
            document.body.style.background = 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)';
        } else {
            document.body.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        }
    }

    function resetSettings() {
        if (confirm('Reset all settings to default?')) {
            localStorage.removeItem('settings');
            loadSettings();
            showNotification('Settings reset to default', 'info');
        }
    }

    function toggleDarkMode(enabled) {
        if (enabled) {
            document.body.style.background = 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)';
        } else {
            document.body.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        }
    }

    function clearData() {
        if (confirm('⚠️ WARNING: This will delete ALL your data. Are you absolutely sure?')) {
            localStorage.clear();
            showNotification('All data cleared', 'warning');
            setTimeout(() => window.location.href = 'index.html', 2000);
        }
    }

    function deleteAccount() {
        if (confirm('🚫 WARNING: This will permanently delete your account. Are you sure?')) {
            localStorage.clear();
            showNotification('Account deleted', 'error');
            setTimeout(() => window.location.href = 'index.html', 2000);
        }
    }

    function showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.textContent = message;

        const colors = {
            success: 'linear-gradient(135deg, #10b981, #059669)',
            info: 'linear-gradient(135deg, #3b82f6, #1d4ed8)',
            warning: 'linear-gradient(135deg, #f59e0b, #d97706)',
            error: 'linear-gradient(135deg, #ef4444, #dc2626)'
        };

        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 25px;
            background: ${colors[type]};
            color: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 4000);
    }
});