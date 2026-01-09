// Logout Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Start automatic logout process
    startLogoutProcess();
});

let logoutProgress = 0;
let logoutInterval;
let isLoggingOut = true;

// Start the logout process
function startLogoutProcess() {
    // Clear any existing login data
    clearLoginData();
    
    // Start progress animation
    logoutInterval = setInterval(updateProgress, 100);
    
    // Auto-complete logout after 3 seconds
    setTimeout(() => {
        if (isLoggingOut) {
            completeLogout();
        }
    }, 3000);
}

// Update progress bar
function updateProgress() {
    if (!isLoggingOut) return;
    
    logoutProgress += 1.5;
    
    if (logoutProgress > 100) {
        logoutProgress = 100;
    }
    
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    
    if (progressFill && progressText) {
        progressFill.style.width = logoutProgress + '%';
        progressText.textContent = Math.round(logoutProgress) + '%';
    }
    
    if (logoutProgress >= 100) {
        clearInterval(logoutInterval);
    }
}

// Cancel logout process
function cancelLogout() {
    isLoggingOut = false;
    clearInterval(logoutInterval);
    
    // Show confirmation dialog
    if (confirm('Are you sure you want to cancel logout?')) {
        // Redirect to dashboard or home
        window.location.href = 'dashboard.html';
    } else {
        // Resume logout process
        isLoggingOut = true;
        startLogoutProcess();
    }
}

// Force immediate logout
function forceLogout() {
    isLoggingOut = false;
    clearInterval(logoutInterval);
    completeLogout();
}

// Complete logout process
function completeLogout() {
    isLoggingOut = false;
    clearInterval(logoutInterval);
    
    // Hide logout content and show success message
    const logoutContent = document.querySelector('.logout-content');
    const logoutSuccess = document.getElementById('logoutSuccess');
    
    if (logoutContent && logoutSuccess) {
        logoutContent.style.display = 'none';
        logoutSuccess.style.display = 'block';
        
        // Add success animation
        logoutSuccess.style.animation = 'fadeInUp 0.6s ease';
    }
    
    // Clear all user data
    clearAllUserData();
    
    // Auto redirect to home page after 5 seconds
    setTimeout(() => {
        window.location.href = 'index.html';
    }, 5000);
}

// Clear login data from localStorage
function clearLoginData() {
    try {
        // Remove login-related data
        localStorage.removeItem('vastologyRememberMe');
        localStorage.removeItem('vastologyUser');
        localStorage.removeItem('userSession');
        localStorage.removeItem('loginTime');
        
        // Remove any other user-specific data
        const keysToRemove = [];
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key && (key.includes('user') || key.includes('login') || key.includes('session'))) {
                keysToRemove.push(key);
            }
        }
        
        keysToRemove.forEach(key => {
            localStorage.removeItem(key);
        });
        
        console.log('Login data cleared successfully');
    } catch (error) {
        console.error('Error clearing login data:', error);
    }
}

// Clear all user data
function clearAllUserData() {
    try {
        // Clear localStorage
        localStorage.clear();
        
        // Clear sessionStorage
        sessionStorage.clear();
        
        // Clear cookies (if any)
        document.cookie.split(";").forEach(function(c) { 
            document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); 
        });
        
        console.log('All user data cleared successfully');
    } catch (error) {
        console.error('Error clearing user data:', error);
    }
}

// Handle page visibility change (if user switches tabs)
document.addEventListener('visibilitychange', function() {
    if (document.hidden && isLoggingOut) {
        // Pause logout process if user switches tabs
        clearInterval(logoutInterval);
    } else if (!document.hidden && isLoggingOut) {
        // Resume logout process when user returns
        logoutInterval = setInterval(updateProgress, 100);
    }
});

// Handle browser back button
window.addEventListener('popstate', function(event) {
    if (isLoggingOut) {
        // Prevent going back during logout
        event.preventDefault();
        history.pushState(null, null, window.location.href);
    }
});

// Prevent page refresh during logout
window.addEventListener('beforeunload', function(event) {
    if (isLoggingOut) {
        event.preventDefault();
        event.returnValue = 'Logout is in progress. Are you sure you want to leave?';
    }
});

// Add keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // ESC key to cancel logout
    if (event.key === 'Escape' && isLoggingOut) {
        cancelLogout();
    }
    
    // Enter key to force logout
    if (event.key === 'Enter' && isLoggingOut) {
        forceLogout();
    }
});

// Show logout confirmation on page load
window.addEventListener('load', function() {
    // Add a subtle notification
    showNotification('Logout process started', 'info');
});

// Notification function
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'info' ? '#3498db' : '#e74c3c'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 10000;
        animation: slideInRight 0.3s ease;
        max-width: 300px;
    `;
    
    document.body.appendChild(notification);
    
    // Remove notification after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

