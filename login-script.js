// Login Form JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('loginForm');
    const inputs = form.querySelectorAll('input');
    
    // Initialize form validation
    initializeLoginValidation();
    
    // Add real-time validation
    inputs.forEach(input => {
        input.addEventListener('blur', validateLoginField);
        input.addEventListener('input', clearLoginError);
    });
    
    // Form submission
    form.addEventListener('submit', handleLoginSubmission);
    
    // Auto-focus on email field
    const emailInput = document.getElementById('email');
    if (emailInput) {
        emailInput.focus();
    }
});

// Initialize login validation
function initializeLoginValidation() {
    const validationRules = {
        email: {
            required: true,
            pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
            message: 'Please enter a valid email address'
        },
        password: {
            required: true,
            minLength: 6,
            message: 'Password must be at least 6 characters'
        }
    };
    
    window.loginValidationRules = validationRules;
}

// Validate individual login field
function validateLoginField(event) {
    const field = event.target;
    const fieldName = field.name;
    const fieldValue = field.value.trim();
    const rules = window.loginValidationRules[fieldName];
    
    if (!rules) return true;
    
    let isValid = true;
    let errorMessage = '';
    
    // Required field validation
    if (rules.required && !fieldValue) {
        isValid = false;
        errorMessage = `${getLoginFieldLabel(fieldName)} is required`;
    }
    
    // Minimum length validation
    if (isValid && rules.minLength && fieldValue.length < rules.minLength) {
        isValid = false;
        errorMessage = rules.message || `${getLoginFieldLabel(fieldName)} must be at least ${rules.minLength} characters`;
    }
    
    // Pattern validation
    if (isValid && rules.pattern && fieldValue && !rules.pattern.test(fieldValue)) {
        isValid = false;
        errorMessage = rules.message || `${getLoginFieldLabel(fieldName)} format is invalid`;
    }
    
    // Update field appearance and error message
    updateLoginFieldValidation(field, isValid, errorMessage);
    
    return isValid;
}

// Clear error when user starts typing
function clearLoginError(event) {
    const field = event.target;
    const errorElement = document.getElementById(field.name + 'Error');
    
    if (errorElement) {
        errorElement.textContent = '';
    }
    
    field.parentElement.classList.remove('error');
    field.parentElement.classList.add('success');
    
    // Remove any existing success/error messages
    removeLoginMessages();
}

// Update login field validation appearance
function updateLoginFieldValidation(field, isValid, errorMessage) {
    const errorElement = document.getElementById(field.name + 'Error');
    const formGroup = field.parentElement;
    
    if (errorElement) {
        errorElement.textContent = errorMessage;
    }
    
    if (isValid) {
        formGroup.classList.remove('error');
        formGroup.classList.add('success');
    } else {
        formGroup.classList.remove('success');
        formGroup.classList.add('error');
    }
}

// Get field label for error messages
function getLoginFieldLabel(fieldName) {
    const labels = {
        email: 'Email',
        password: 'Password'
    };
    return labels[fieldName] || fieldName;
}

// Toggle password visibility
function togglePassword(fieldId) {
    const field = document.getElementById(fieldId);
    const toggle = field.parentElement.querySelector('.password-toggle i');
    
    if (field.type === 'password') {
        field.type = 'text';
        toggle.classList.remove('fa-eye');
        toggle.classList.add('fa-eye-slash');
    } else {
        field.type = 'password';
        toggle.classList.remove('fa-eye-slash');
        toggle.classList.add('fa-eye');
    }
}

// Handle login form submission
function handleLoginSubmission(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitButton = form.querySelector('.login-btn');
    
    // Validate all fields
    const isValid = validateAllLoginFields();
    
    if (isValid) {
        // Show loading state
        submitButton.classList.add('loading');
        submitButton.disabled = true;
        
        // Get form data
        const formData = new FormData(form);
        const loginData = {
            email: formData.get('email'),
            password: formData.get('password'),
            rememberMe: formData.get('rememberMe') === 'on'
        };
        
        // Simulate login API call
        simulateLogin(loginData);
    } else {
        // Scroll to first error
        const firstError = form.querySelector('.error');
        if (firstError) {
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }
}

// Validate all login form fields
function validateAllLoginFields() {
    const form = document.getElementById('loginForm');
    const inputs = form.querySelectorAll('input[required]');
    let allValid = true;
    
    inputs.forEach(input => {
        const event = { target: input };
        const isValid = validateLoginField(event);
        if (!isValid) allValid = false;
    });
    
    return allValid;
}

// Real login API call
async function simulateLogin(loginData) {
    try {
        const response = await fetch('login_process.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(loginData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showLoginSuccess();
            
            // Redirect to dashboard after success
            setTimeout(() => {
                window.location.href = result.redirect || 'dashboard.php';
            }, 1500);
        } else {
            showLoginError(result.message || 'Invalid email or password');
            
            // Reset button state
            const submitButton = document.querySelector('.login-btn');
            submitButton.classList.remove('loading');
            submitButton.disabled = false;
        }
    } catch (error) {
        console.error('Login error:', error);
        showLoginError('Login failed. Please try again.');
        
        // Reset button state
        const submitButton = document.querySelector('.login-btn');
        submitButton.classList.remove('loading');
        submitButton.disabled = false;
    }
}

// Show login success message
function showLoginSuccess() {
    removeLoginMessages();
    
    const successDiv = document.createElement('div');
    successDiv.className = 'login-success';
    successDiv.innerHTML = `
        <i class="fas fa-check-circle"></i>
        Login successful! Redirecting to dashboard...
    `;
    
    const form = document.getElementById('loginForm');
    form.insertBefore(successDiv, form.firstChild);
}

// Show login error message
function showLoginError(message) {
    removeLoginMessages();
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'login-error';
    errorDiv.innerHTML = `
        <i class="fas fa-exclamation-circle"></i>
        ${message}
    `;
    
    const form = document.getElementById('loginForm');
    form.insertBefore(errorDiv, form.firstChild);
}

// Remove existing messages
function removeLoginMessages() {
    const existingMessages = document.querySelectorAll('.login-success, .login-error');
    existingMessages.forEach(msg => msg.remove());
}

// Social login functionality
function socialLogin(provider) {
    const socialButton = document.querySelector(`.${provider}-btn`);
    
    // Add loading state
    socialButton.style.opacity = '0.7';
    socialButton.style.cursor = 'not-allowed';
    
    // Simulate social login
    setTimeout(() => {
        showLoginSuccess();
        
        // Reset button state
        socialButton.style.opacity = '1';
        socialButton.style.cursor = 'pointer';
        
        // Redirect to dashboard
        setTimeout(() => {
            window.location.href = 'dashboard.html';
        }, 2000);
    }, 1000);
}

// Check for existing login session (disabled auto-login)
function checkExistingSession() {
    // Auto-login disabled - users must manually login each time
    // This prevents automatic login after page refresh
    return false;
}

// Initialize session check (disabled)
document.addEventListener('DOMContentLoaded', function() {
    // Auto-login functionality removed
    // Users need to manually login each time
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Enter key to submit form
    if (e.key === 'Enter' && !e.shiftKey) {
        const form = document.getElementById('loginForm');
        const activeElement = document.activeElement;
        
        if (form.contains(activeElement)) {
            e.preventDefault();
            form.dispatchEvent(new Event('submit'));
        }
    }
    
    // Escape key to clear errors
    if (e.key === 'Escape') {
        removeLoginMessages();
        clearAllErrors();
    }
});

// Clear all form errors
function clearAllErrors() {
    const form = document.getElementById('loginForm');
    const errorElements = form.querySelectorAll('.error-message');
    const formGroups = form.querySelectorAll('.form-group');
    
    errorElements.forEach(element => {
        element.textContent = '';
    });
    
    formGroups.forEach(group => {
        group.classList.remove('error', 'success');
    });
}

// Form auto-save for remember me (disabled)
function autoSaveLoginForm() {
    // Auto-save disabled - prevents saving form data
    // Users must enter details manually each time
    return false;
}

// Load saved form data (disabled)
function loadSavedLoginForm() {
    // Auto-fill disabled - users must enter details manually each time
    // This prevents auto-filling form after page refresh
    return false;
}

// Initialize auto-save (disabled)
document.addEventListener('DOMContentLoaded', function() {
    // Auto-save and auto-fill functionality removed
    // Users need to enter login details manually each time
});

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Demo credentials display (for development)
function showDemoCredentials() {
    const demoDiv = document.createElement('div');
    demoDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--primary);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        font-size: 0.9rem;
        z-index: 1000;
        max-width: 250px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    `;
    demoDiv.innerHTML = `
        <strong>Demo Credentials:</strong><br>
        Email: demo@vastuvision.com<br>
        Password: demo123
    `;
    
    document.body.appendChild(demoDiv);
    
    // Auto-remove after 10 seconds
    setTimeout(() => {
        demoDiv.remove();
    }, 10000);
}

// Show demo credentials in development
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    document.addEventListener('DOMContentLoaded', function() {
        setTimeout(showDemoCredentials, 2000);
    });
}
