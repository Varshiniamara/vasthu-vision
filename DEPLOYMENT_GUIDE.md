# Vastu Vision - Complete Deployment Guide

## 📋 Prerequisites

1. ✅ PHP 7.4 or higher
2. ✅ MySQL 5.7 or higher
3. ✅ Apache web server with mod_rewrite enabled
4. ✅ phpMyAdmin access
5. ✅ HTTPS/SSL certificate (recommended)

---

## 🚀 Step-by-Step Deployment

### **Step 1: Database Setup**

1. **Login to phpMyAdmin**
   - Go to: `https://vastology.purlyedit.in/phpmyadmin`
   - Login with your credentials

2. **Create Database**
   - Click "New" in left sidebar
   - Database name: `vastu_vision`
   - Collation: `utf8mb4_general_ci`
   - Click "Create"

3. **Import Database Schema**
   - Select `vastu_vision` database
   - Click "Import" tab
   - Choose file: `database.sql`
   - Click "Go"
   - ✅ All tables should be created

### **Step 2: Update Configuration**

Edit `config.php` with your database credentials:

```php
define('DB_HOST', 'localhost');
define('DB_NAME', 'vastu_vision');
define('DB_USER', 'your_db_username');      // Update this
define('DB_PASS', 'your_db_password');      // Update this
define('SITE_URL', 'https://vastology.purlyedit.in');
```

### **Step 3: File Upload**

Upload ALL files to your server:

#### **Required Files:**
```
/public_html/
├── config.php
├── Database.php
├── .htaccess
├── register.php
├── register_process.php
├── login.html
├── login_process.php
├── logout.php
├── dashboard.php
├── space.php
├── space_save.php
├── upload_floor_plan.php
├── api_get_user_data.php
├── styles.css
├── register-styles.css
├── login-styles.css
├── space-styles.css
├── dashboard-styles.css
├── vastu-animations.css
├── register-script.js
├── login-script.js
├── space-script.js
├── dashboard-script.js
├── script.js
├── index.html
└── uploads/ (folder - create this)
```

### **Step 4: Set Permissions**

Set correct permissions for uploads folder:
```bash
chmod 755 uploads/
```

Or via FTP/cPanel: Set folder permission to `755`

### **Step 5: Test Backend Connection**

1. **Test Database Connection:**
   Create a test file `test_db.php`:
   ```php
   <?php
   require_once 'config.php';
   require_once 'Database.php';
   
   try {
       $db = Database::getInstance()->getConnection();
       echo "✅ Database connected successfully!";
   } catch (Exception $e) {
       echo "❌ Database connection failed: " . $e->getMessage();
   }
   ```
   
   Visit: `https://vastology.purlyedit.in/test_db.php`
   Should show: "✅ Database connected successfully!"
   **Delete this file after testing!**

2. **Test Registration:**
   - Go to: `https://vastology.purlyedit.in/register.php`
   - Fill in the form
   - Click "Create Account"
   - Should see success message
   - Check phpMyAdmin → users table for new entry

3. **Test Login:**
   - Go to: `https://vastology.purlyedit.in/login.html`
   - Enter registered credentials
   - Should redirect to dashboard.php

4. **Test Space Save:**
   - Login first
   - Go to dashboard
   - Click "Space Details"
   - Fill in space form
   - Submit
   - Check phpMyAdmin → spaces & rooms tables

---

## 🔧 API Endpoints

### **Authentication APIs**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/register_process.php` | POST | User registration |
| `/login_process.php` | POST | User login |
| `/logout.php` | GET | User logout |

### **Space Management APIs**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/space_save.php` | POST | Save space & rooms |
| `/api_get_user_data.php` | GET | Get user spaces |

### **File Upload APIs**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/upload_floor_plan.php` | POST | Upload floor plans |

---

## 📝 Update Login Form

Update `login.html` to connect to backend:

Add this script before `</body>`:

```javascript
<script>
document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const loginBtn = document.getElementById('loginBtn');
    const originalText = loginBtn.innerHTML;
    
    loginBtn.disabled = true;
    loginBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Logging in...';
    
    const formData = {
        email: document.getElementById('email').value.trim(),
        password: document.getElementById('password').value,
        rememberMe: document.getElementById('remember').checked
    };
    
    try {
        const response = await fetch('login_process.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            window.location.href = result.redirect;
        } else {
            alert(result.message);
            loginBtn.disabled = false;
            loginBtn.innerHTML = originalText;
        }
    } catch (error) {
        alert('Network error. Please try again.');
        loginBtn.disabled = false;
        loginBtn.innerHTML = originalText;
    }
});
</script>
```

---

## 🔐 Security Checklist

- [ ] Update `config.php` with real database credentials
- [ ] Set proper file permissions (uploads: 755)
- [ ] Enable HTTPS (SSL certificate)
- [ ] Delete `test_db.php` after testing
- [ ] Set `display_errors = Off` in production
- [ ] Regular database backups
- [ ] Keep PHP version updated
- [ ] Monitor error logs

---

## 🐛 Troubleshooting

### Issue: Database Connection Failed
**Solution:**
- Check database credentials in `config.php`
- Verify database exists in phpMyAdmin
- Check if user has proper permissions

### Issue: 500 Internal Server Error
**Solution:**
- Check PHP error logs
- Verify .htaccess syntax
- Ensure PHP version is 7.4+

### Issue: Files Not Uploading
**Solution:**
- Check `uploads/` folder exists
- Verify folder permissions (755)
- Check PHP `upload_max_filesize` setting

### Issue: Session Not Working
**Solution:**
- Verify session directory is writable
- Check PHP session settings
- Clear browser cookies

---

## 📊 Database Tables Overview

| Table | Purpose |
|-------|---------|
| `users` | User accounts |
| `spaces` | User's space details |
| `rooms` | Rooms with zones |
| `floor_plans` | Uploaded files |
| `analysis_results` | Vastu analysis |
| `user_sessions` | Session management |
| `activity_log` | User activity tracking |

---

## 🎯 Testing Checklist

- [ ] Register new user
- [ ] Login with credentials
- [ ] Access dashboard
- [ ] Upload floor plan
- [ ] Create space with rooms
- [ ] Save space details
- [ ] Logout
- [ ] Login again (session persistence)

---

## 📞 Support

If you encounter any issues:
1. Check error logs
2. Verify all files are uploaded
3. Test database connection
4. Check browser console for JavaScript errors

---

## 🎉 Deployment Complete!

Your Vastu Vision application is now live at:
**https://vastology.purlyedit.in**

All backend APIs are connected and ready to use!

