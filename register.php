<?php
require_once 'config.php';

// If already logged in, redirect to dashboard
if (isset($_SESSION['logged_in']) && $_SESSION['logged_in'] === true) {
    header('Location: dashboard.php');
    exit;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register - Vastu Vision</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="register-styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-logo">
                <i class="fas fa-home"></i>
                <span>Vastu Vision</span>
            </div>
            <ul class="nav-menu">
                <li><a href="index.html">Home</a></li>
                <li><a href="index.html#features">Features</a></li>
                <li><a href="index.html#about">About</a></li>
                <li><a href="index.html#contact">Contact</a></li>
            </ul>
            <div class="nav-buttons">
                <a href="login.html" class="btn-login">Login</a>
                <a href="register.php" class="btn-register">Register</a>
            </div>
        </div>
    </nav>

    <!-- Register Section -->
    <section class="register-section">
        <div class="register-container">
            <div class="register-header">
                <h1>Join Vastu Vision</h1>
                <p>Create your account to start designing harmonious spaces</p>
            </div>

            <div class="register-form-container">
                <form class="register-form" id="registerForm">
                    <!-- Personal Information -->
                    <div class="form-section">
                        <h3><i class="fas fa-user"></i> Personal Information</h3>
                        
                        <div class="form-row">
                            <div class="form-group">
                                <label for="firstName">First Name *</label>
                                <input type="text" id="firstName" name="firstName" required autocomplete="off">
                                <span class="error-message" id="firstNameError"></span>
                            </div>

                            <div class="form-group">
                                <label for="lastName">Last Name *</label>
                                <input type="text" id="lastName" name="lastName" required autocomplete="off">
                                <span class="error-message" id="lastNameError"></span>
                            </div>
                        </div>

                        <div class="form-group">
                            <label for="email">Email Address *</label>
                            <input type="email" id="email" name="email" required autocomplete="off">
                            <span class="error-message" id="emailError"></span>
                        </div>

                        <div class="form-group">
                            <label for="phone">Phone Number *</label>
                            <input type="tel" id="phone" name="phone" required placeholder="10-digit mobile number" autocomplete="off">
                            <span class="error-message" id="phoneError"></span>
                        </div>

                        <div class="form-row">
                            <div class="form-group">
                                <label for="gender">Gender *</label>
                                <select id="gender" name="gender" required>
                                    <option value="">Select Gender</option>
                                    <option value="male">Male</option>
                                    <option value="female">Female</option>
                                    <option value="other">Other</option>
                                    <option value="prefer-not-to-say">Prefer not to say</option>
                                </select>
                                <span class="error-message" id="genderError"></span>
                            </div>

                            <div class="form-group">
                                <label for="dateOfBirth">Date of Birth</label>
                                <input type="date" id="dateOfBirth" name="dateOfBirth" autocomplete="off">
                                <span class="error-message" id="dateOfBirthError"></span>
                            </div>
                        </div>
                    </div>

                    <!-- Account Security -->
                    <div class="form-section">
                        <h3><i class="fas fa-lock"></i> Account Security</h3>
                        
                        <div class="form-group">
                            <label for="password">Password *</label>
                            <div class="password-input-wrapper">
                                <input type="password" id="password" name="password" required autocomplete="new-password">
                                <button type="button" class="toggle-password" onclick="togglePassword('password')">
                                    <i class="fas fa-eye"></i>
                                </button>
                            </div>
                            <div class="password-strength" id="passwordStrength">
                                <div class="strength-bar"></div>
                                <span class="strength-text">Password strength</span>
                            </div>
                            <span class="error-message" id="passwordError"></span>
                        </div>

                        <div class="form-group">
                            <label for="confirmPassword">Confirm Password *</label>
                            <div class="password-input-wrapper">
                                <input type="password" id="confirmPassword" name="confirmPassword" required autocomplete="new-password">
                                <button type="button" class="toggle-password" onclick="togglePassword('confirmPassword')">
                                    <i class="fas fa-eye"></i>
                                </button>
                            </div>
                            <span class="error-message" id="confirmPasswordError"></span>
                        </div>
                    </div>

                    <button type="submit" class="btn-register-submit" id="registerBtn">
                        <i class="fas fa-user-plus"></i>
                        Create Account
                    </button>
                </form>

                <div class="register-footer">
                    <p>Already have an account? <a href="login.html">Sign in here</a></p>
                </div>
            </div>

            <!-- Success/Error Message Display -->
            <div id="messageContainer" style="display: none;"></div>
        </div>
    </section>

    <script src="register-script.js"></script>
    <script>
        // Override form submission to use backend API
        document.getElementById('registerForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const registerBtn = document.getElementById('registerBtn');
            const originalText = registerBtn.innerHTML;
            
            // Show loading state
            registerBtn.disabled = true;
            registerBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating Account...';
            
            // Collect form data
            const formData = {
                firstName: document.getElementById('firstName').value.trim(),
                lastName: document.getElementById('lastName').value.trim(),
                email: document.getElementById('email').value.trim(),
                phone: document.getElementById('phone').value.trim(),
                gender: document.getElementById('gender').value,
                dateOfBirth: document.getElementById('dateOfBirth').value,
                password: document.getElementById('password').value,
                confirmPassword: document.getElementById('confirmPassword').value
            };
            
            try {
                const response = await fetch('register_process.php', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    // Show success message
                    showMessage(result.message, 'success');
                    
                    // Redirect to login after 2 seconds
                    setTimeout(() => {
                        window.location.href = 'login.html';
                    }, 2000);
                } else {
                    // Show error message
                    showMessage(result.message, 'error');
                    registerBtn.disabled = false;
                    registerBtn.innerHTML = originalText;
                }
                
            } catch (error) {
                console.error('Registration error:', error);
                showMessage('Network error. Please try again.', 'error');
                registerBtn.disabled = false;
                registerBtn.innerHTML = originalText;
            }
        });
        
        function showMessage(message, type) {
            const container = document.getElementById('messageContainer');
            container.style.display = 'block';
            container.className = `message-box ${type}`;
            container.innerHTML = `
                <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
                <span>${message}</span>
            `;
            
            container.scrollIntoView({ behavior: 'smooth', block: 'center' });
            
            if (type === 'error') {
                setTimeout(() => {
                    container.style.display = 'none';
                }, 5000);
            }
        }
        
        function togglePassword(fieldId) {
            const field = document.getElementById(fieldId);
            const button = field.nextElementSibling;
            const icon = button.querySelector('i');
            
            if (field.type === 'password') {
                field.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                field.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        }
    </script>
    
    <style>
        .message-box {
            max-width: 600px;
            margin: 2rem auto;
            padding: 1.5rem;
            border-radius: 10px;
            display: flex;
            align-items: center;
            gap: 1rem;
            font-size: 1rem;
            animation: slideDown 0.3s ease;
        }
        
        .message-box.success {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        
        .message-box.error {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }
        
        .message-box i {
            font-size: 1.5rem;
        }
        
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
</body>
</html>

