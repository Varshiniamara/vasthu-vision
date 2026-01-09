// Registration Form JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registerForm');
    const inputs = form.querySelectorAll('input, select');
    
    // Initialize form validation
    initializeFormValidation();
    
    // Add real-time validation
    inputs.forEach(input => {
        input.addEventListener('blur', validateField);
        input.addEventListener('input', clearError);
    });
    
    // Password strength checker
    const passwordInput = document.getElementById('password');
    if (passwordInput) {
        passwordInput.addEventListener('input', checkPasswordStrength);
    }
    
    // Confirm password validation
    const confirmPasswordInput = document.getElementById('confirmPassword');
    if (confirmPasswordInput) {
        confirmPasswordInput.addEventListener('input', validateConfirmPassword);
    }
    
    // Form submission
    form.addEventListener('submit', handleFormSubmission);
});

// Initialize form validation
function initializeFormValidation() {
    // Add validation rules
    const validationRules = {
        firstName: {
            required: true,
            minLength: 2,
            pattern: /^[a-zA-Z\s]+$/,
            message: 'First name must be at least 2 characters and contain only letters'
        },
        lastName: {
            required: true,
            minLength: 2,
            pattern: /^[a-zA-Z\s]+$/,
            message: 'Last name must be at least 2 characters and contain only letters'
        },
        email: {
            required: true,
            pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
            message: 'Please enter a valid email address'
        },
        phone: {
            required: true,
            pattern: /^[6-9]\d{4}\s\d{5}$/,
            message: 'Please enter a valid 10-digit Indian mobile number'
        },
        gender: {
            required: true,
            message: 'Please select your gender'
        },
        password: {
            required: true,
            minLength: 8,
            pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/,
            message: 'Password must be at least 8 characters with uppercase, lowercase, number and special character'
        },
        confirmPassword: {
            required: true,
            message: 'Passwords do not match'
        },
    };
    
    // Store validation rules globally
    window.validationRules = validationRules;
}

// Validate individual field
function validateField(event) {
    const field = event.target;
    const fieldName = field.name;
    const fieldValue = field.value.trim();
    const rules = window.validationRules[fieldName];
    
    if (!rules) return true;
    
    let isValid = true;
    let errorMessage = '';
    
    // Required field validation
    if (rules.required && !fieldValue) {
        isValid = false;
        errorMessage = `${getFieldLabel(fieldName)} is required`;
    }
    
    // Minimum length validation
    if (isValid && rules.minLength && fieldValue.length < rules.minLength) {
        isValid = false;
        errorMessage = rules.message || `${getFieldLabel(fieldName)} must be at least ${rules.minLength} characters`;
    }
    
    // Pattern validation
    if (isValid && rules.pattern && fieldValue && !rules.pattern.test(fieldValue)) {
        // Special handling for phone number - check both formatted and unformatted
        if (fieldName === 'phone') {
            const cleanPhone = fieldValue.replace(/\s/g, '');
            const phonePattern = /^[6-9]\d{9}$/;
            if (!phonePattern.test(cleanPhone)) {
                isValid = false;
                errorMessage = rules.message || `${getFieldLabel(fieldName)} format is invalid`;
            }
        } else {
            isValid = false;
            errorMessage = rules.message || `${getFieldLabel(fieldName)} format is invalid`;
        }
    }
    
    // Special validation for confirm password
    if (fieldName === 'confirmPassword' && fieldValue) {
        const password = document.getElementById('password').value;
        if (fieldValue !== password) {
            isValid = false;
            errorMessage = 'Passwords do not match';
        }
    }
    
    // Update field appearance and error message
    updateFieldValidation(field, isValid, errorMessage);
    
    return isValid;
}

// Clear error when user starts typing
function clearError(event) {
    const field = event.target;
    const errorElement = document.getElementById(field.name + 'Error');
    
    if (errorElement) {
        errorElement.textContent = '';
    }
    
    field.parentElement.classList.remove('error');
    field.parentElement.classList.add('success');
}

// Update field validation appearance
function updateFieldValidation(field, isValid, errorMessage) {
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
function getFieldLabel(fieldName) {
    const labels = {
        firstName: 'First Name',
        lastName: 'Last Name',
        email: 'Email',
        phone: 'Phone Number',
        gender: 'Gender',
        password: 'Password',
        confirmPassword: 'Confirm Password',
    };
    return labels[fieldName] || fieldName;
}

// Check password strength
function checkPasswordStrength(event) {
    const password = event.target.value;
    const strengthFill = document.getElementById('strengthFill');
    const strengthText = document.getElementById('strengthText');
    
    if (!strengthFill || !strengthText) return;
    
    let strength = 0;
    let strengthLabel = '';
    
    // Check password criteria
    if (password.length >= 8) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[@$!%*?&]/.test(password)) strength++;
    
    // Update strength indicator
    strengthFill.className = 'strength-fill';
    
    if (password.length === 0) {
        strengthLabel = 'Password strength';
        strengthFill.style.width = '0%';
    } else if (strength <= 2) {
        strengthLabel = 'Weak';
        strengthFill.classList.add('weak');
    } else if (strength <= 3) {
        strengthLabel = 'Fair';
        strengthFill.classList.add('fair');
    } else if (strength <= 4) {
        strengthLabel = 'Good';
        strengthFill.classList.add('good');
    } else {
        strengthLabel = 'Strong';
        strengthFill.classList.add('strong');
    }
    
    strengthText.textContent = strengthLabel;
}

// Validate confirm password
function validateConfirmPassword(event) {
    const confirmPassword = event.target.value;
    const password = document.getElementById('password').value;
    
    if (confirmPassword && password && confirmPassword !== password) {
        updateFieldValidation(event.target, false, 'Passwords do not match');
        return false;
    } else if (confirmPassword && password && confirmPassword === password) {
        updateFieldValidation(event.target, true, '');
        return true;
    }
    
    return true;
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

// Handle form submission
async function handleFormSubmission(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitButton = form.querySelector('button[type="submit"]');
    
    // Validate all fields
    const isValid = validateAllFields();
    
    if (isValid) {
        // Show loading state
        submitButton.classList.add('loading');
        submitButton.disabled = true;
        
        // Collect form data
        const formData = new FormData(form);
        const registerData = {
            firstName: formData.get('firstName'),
            lastName: formData.get('lastName'),
            email: formData.get('email'),
            phone: formData.get('phone'),
            gender: formData.get('gender'),
            dateOfBirth: formData.get('dateOfBirth'),
            password: formData.get('password'),
            confirmPassword: formData.get('confirmPassword')
        };
        
        try {
            const response = await fetch('register_process.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(registerData)
            });
            
            const result = await response.json();
            
            if (result.success) {
                showSuccessMessage();
                
                // Redirect to dashboard or login
                setTimeout(() => {
                    window.location.href = result.redirect || 'dashboard.php';
                }, 2000);
            } else {
                showErrorMessage(result.message || 'Registration failed. Please try again.');
                submitButton.classList.remove('loading');
                submitButton.disabled = false;
            }
        } catch (error) {
            console.error('Registration error:', error);
            showErrorMessage('Registration failed. Please try again.');
            submitButton.classList.remove('loading');
            submitButton.disabled = false;
        }
    } else {
        // Scroll to first error
        const firstError = form.querySelector('.error');
        if (firstError) {
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }
}

// Show error message
function showErrorMessage(message) {
    const form = document.getElementById('registerForm');
    const existingError = form.querySelector('.form-error-message');
    if (existingError) {
        existingError.remove();
    }
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'form-error-message';
    errorDiv.style.cssText = `
        background: #ff4757;
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    `;
    errorDiv.innerHTML = `
        <i class="fas fa-exclamation-circle"></i>
        <span>${message}</span>
    `;
    
    form.insertBefore(errorDiv, form.firstChild);
    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Validate all form fields
function validateAllFields() {
    const form = document.getElementById('registerForm');
    const inputs = form.querySelectorAll('input[required], select[required]');
    let allValid = true;
    
    inputs.forEach(input => {
        const event = { target: input };
        const isValid = validateField(event);
        if (!isValid) allValid = false;
    });
    
    return allValid;
}


// Show success message
function showSuccessMessage(message = 'Registration successful! Welcome to Vastu Vision!') {
    // Create success modal
    const modal = document.createElement('div');
    modal.className = 'success-modal';
    modal.innerHTML = `
        <div class="success-content">
            <div class="success-icon">
                <i class="fas fa-check-circle"></i>
            </div>
            <h3>Registration Successful!</h3>
            <p>${message}</p>
            <button class="btn-primary" onclick="closeSuccessModal()">Continue</button>
        </div>
    `;
    
    // Add modal styles
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 10000;
        animation: fadeIn 0.3s ease;
    `;
    
    const successContent = modal.querySelector('.success-content');
    successContent.style.cssText = `
        background: white;
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        max-width: 400px;
        width: 90%;
        animation: slideUp 0.3s ease;
    `;
    
    const successIcon = modal.querySelector('.success-icon');
    successIcon.style.cssText = `
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #2A9D8F, #1E8449);
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto 1.5rem;
        color: white;
        font-size: 2.5rem;
    `;
    
    document.body.appendChild(modal);
    
    // Add CSS animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes slideUp {
            from { transform: translateY(30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
    `;
    document.head.appendChild(style);
}

// Close success modal
function closeSuccessModal() {
    const modal = document.querySelector('.success-modal');
    if (modal) {
        modal.remove();
    }
    
    // Redirect to login page or dashboard
    setTimeout(() => {
        window.location.href = 'index.html';
    }, 1000);
}

// Indian phone number formatting
document.getElementById('phone').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');
    
    // Limit to 10 digits for Indian mobile numbers
    if (value.length > 10) {
        value = value.slice(0, 10);
    }
    
    // Format as Indian mobile number: XXXXX XXXXX
    if (value.length > 5) {
        value = value.slice(0, 5) + ' ' + value.slice(5);
    }
    
    e.target.value = value;
});

// Form auto-save (disabled)
function autoSaveForm() {
    // Auto-save disabled - prevents saving form data
    // Users must enter details manually each time
    return false;
}

// Load saved form data (disabled)
function loadSavedForm() {
    // Auto-fill disabled - users must enter details manually each time
    // This prevents auto-filling form after page refresh
    return false;
}

// Initialize auto-save (disabled)
document.addEventListener('DOMContentLoaded', function() {
    // Auto-save and auto-fill functionality removed
    // Users need to enter registration details manually each time
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
