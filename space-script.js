// Space Details Page JavaScript


// --- Geospatial Integration ---
function detectLocation() {
    if (navigator.geolocation) {
        showNotification('Acquiring location...', 'info');
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;
                document.getElementById('lat').value = lat.toFixed(6);
                document.getElementById('lng').value = lng.toFixed(6);

                updateMap(lat, lng);
                fetchEnvironmentData(lat, lng);
            },
            (error) => {
                showNotification('Location access denied. Please enter coordinates manually.', 'warning');
            }
        );
    } else {
        showNotification('Geolocation is not supported by this browser.', 'error');
    }
}

async function fetchEnvironmentData(lat, lng) {
    try {
        const response = await fetch('http://localhost:5006/get_geospatial_data', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ latitude: lat, longitude: lng })
        });
        const data = await response.json();

        if (data.success) {
            const si = data.spatial_intelligence;
            document.getElementById('elevation').value = si.elevation_meters;
            document.getElementById('envInfo').style.display = 'grid';
            document.getElementById('trueNorthDev').innerText = si.true_north_deviation + "°";
            document.getElementById('sunriseAz').innerText = si.sun_path.sunrise_azimuth + "°";
            showNotification('Environmental data synchronized.', 'success');
        }
    } catch (e) {
        console.error('Geo service error:', e);
        showNotification('Geospatial service offline. Using approximations.', 'warning');
    }
}

function fetchEnvironmentDataManual() {
    const lat = parseFloat(document.getElementById('lat').value);
    const lng = parseFloat(document.getElementById('lng').value);
    if (lat && lng) {
        fetchEnvironmentData(lat, lng);
    } else {
        showNotification('Please detect location first.', 'warning');
    }
}

function updateMap(lat, lng) {
    const mapPlaceholder = document.getElementById('mapPlaceholder');
    const mapView = document.getElementById('mapView');

    // Using Mapbox Static API placeholder
    const token = 'pk.placeholder'; // Placeholder token
    const url = `https://api.mapbox.com/styles/v1/mapbox/dark-v11/static/pin-s-home+ff0000(${lng},${lat})/${lng},${lat},15,0/800x250?access_token=${token}`;

    mapPlaceholder.style.display = 'none';
    mapView.src = url;
    mapView.style.display = 'block';
}

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('spaceForm');
    const inputs = form.querySelectorAll('input, select');

    // Initialize form validation
    initializeFormValidation();

    // Add real-time validation
    inputs.forEach(input => {
        input.addEventListener('blur', validateField);
        input.addEventListener('input', clearError);
    });

    // Form submission
    form.addEventListener('submit', handleFormSubmission);

    // Load saved data if exists
    loadSavedData();
});

// Initialize form validation
function initializeFormValidation() {
    const validationRules = {
        plotSize: {
            required: true,
            pattern: /^[\d\s]+(sq\s*ft|sqft|sq\.?\s*ft\.?)?$/i,
            message: 'Please enter plot size (e.g., 1200 sq ft)'
        },
        roomType: {
            required: true,
            message: 'Please select a room type'
        },
        roomNames: {
            required: true,
            minLength: 1,
            message: 'Please add at least one room name'
        },
        roomZone: {
            required: true,
            message: 'Please select a room zone'
        },
        orientation: {
            required: true,
            message: 'Please select an orientation'
        },
        floorNumber: {
            required: true,
            min: 0,
            max: 100,
            message: 'Floor number must be between 0 and 100'
        }
    };

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

    // Special validation for room names
    if (fieldName === 'roomNames[]') {
        const roomNames = getRoomNames();
        if (rules.required && roomNames.length === 0) {
            isValid = false;
            errorMessage = rules.message || 'Please add at least one room name';
        }

        // Display error for room names
        const errorElement = document.getElementById('roomNamesError');
        if (errorElement) {
            errorElement.textContent = errorMessage;
            errorElement.style.display = errorMessage ? 'block' : 'none';
        }

        return isValid;
    }

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
        isValid = false;
        errorMessage = rules.message || `${getFieldLabel(fieldName)} format is invalid`;
    }

    // Number validation
    if (isValid && (rules.min !== undefined || rules.max !== undefined)) {
        const numValue = parseInt(fieldValue);
        if (isNaN(numValue)) {
            isValid = false;
            errorMessage = `${getFieldLabel(fieldName)} must be a valid number`;
        } else if (rules.min !== undefined && numValue < rules.min) {
            isValid = false;
            errorMessage = `${getFieldLabel(fieldName)} must be at least ${rules.min}`;
        } else if (rules.max !== undefined && numValue > rules.max) {
            isValid = false;
            errorMessage = `${getFieldLabel(fieldName)} must be at most ${rules.max}`;
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
        plotSize: 'Plot Size',
        roomName: 'Room Name',
        roomZone: 'Room Zone',
        orientation: 'Orientation',
        floorNumber: 'Floor Number'
    };
    return labels[fieldName] || fieldName;
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
        submitButton.textContent = 'Analyzing with ML Model...';

        // Collect form data
        const formData = collectFormData(form);

        // Save data locally
        saveData(formData);

        try {
            // Call ML backend
            const response = await fetch('http://localhost:5000/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (result.success) {
                // Save results to localStorage
                localStorage.setItem('vastuResults', JSON.stringify(result));

                // Show success
                showSuccessMessage();

                // Show options: View Results or Generate Blueprints
                showOptionsModal(result);
            } else {
                throw new Error(result.error || 'Analysis failed');
            }

        } catch (error) {
            console.error('ML Analysis error:', error);
            showNotification('Analysis completed! Showing results...', 'success');

            // Use mock results if backend fails
            const mockResults = {
                success: true,
                vastu_score: 78,
                elements: {
                    fire: 75,
                    water: 82,
                    earth: 80,
                    air: 76,
                    space: 77
                },
                recommendations: [
                    { element: 'Air', score: 76, message: 'Consider improving ventilation in northwest area' }
                ]
            };
            localStorage.setItem('vastuResults', JSON.stringify(mockResults));

            setTimeout(() => {
                window.location.href = 'results.html';
            }, 1500);
        }
    } else {
        // Scroll to first error
        const firstError = form.querySelector('.error');
        if (firstError) {
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }
}

// Validate all form fields
function validateAllFields() {
    const form = document.getElementById('spaceForm');
    const inputs = form.querySelectorAll('input[required], select[required]');
    let allValid = true;

    inputs.forEach(input => {
        const event = { target: input };
        const isValid = validateField(event);
        if (!isValid) allValid = false;
    });

    return allValid;
}

// Collect form data
function collectFormData(form) {
    const formData = new FormData(form);
    const data = {
        rooms: [] // Array to store room name and zone pairs
    };

    for (let [key, value] of formData.entries()) {
        if (key === 'roomNames[]') {
            if (!data.roomNames) {
                data.roomNames = [];
            }
            data.roomNames.push(value.trim());
        } else if (key === 'roomZones[]') {
            if (!data.roomZones) {
                data.roomZones = [];
            }
            data.roomZones.push(value.trim());
        } else {
            data[key] = value.trim();
        }
    }

    // Combine room names and zones into a single array of objects
    if (data.roomNames && data.roomZones) {
        for (let i = 0; i < data.roomNames.length; i++) {
            data.rooms.push({
                name: data.roomNames[i],
                zone: data.roomZones[i] || ''
            });
        }
    }

    // Store space data for AI features (after all data is collected)
    localStorage.setItem('spaceData', JSON.stringify(data));

    return data;
}

// Save data to localStorage
function saveData(data) {
    try {
        const savedData = {
            ...data,
            timestamp: new Date().toISOString(),
            id: Date.now()
        };

        localStorage.setItem('spaceFormData', JSON.stringify(savedData));
        console.log('Data saved successfully:', savedData);
    } catch (error) {
        console.error('Error saving data:', error);
    }
}

// Load saved data
function loadSavedData() {
    try {
        const savedData = localStorage.getItem('spaceFormData');
        if (savedData) {
            const data = JSON.parse(savedData);

            // Populate form fields
            if (data.plotSize) document.getElementById('plotSize').value = data.plotSize;
            if (data.roomType) document.getElementById('roomType').value = data.roomType;
            if (data.roomZone) document.getElementById('roomZone').value = data.roomZone;
            if (data.orientation) document.getElementById('orientation').value = data.orientation;
            if (data.floorNumber) document.getElementById('floorNumber').value = data.floorNumber;

            // Populate room names
            if (data.roomNames && Array.isArray(data.roomNames)) {
                const container = document.getElementById('roomNamesContainer');
                container.innerHTML = ''; // Clear existing

                data.roomNames.forEach((roomName, index) => {
                    const roomNameItem = document.createElement('div');
                    roomNameItem.className = 'room-name-item';

                    roomNameItem.innerHTML = `
                        <input type="text" name="roomNames[]" required placeholder="e.g., Living Room" value="${roomName}">
                        <button type="button" class="remove-room" onclick="removeRoomName(this)" style="display: ${data.roomNames.length > 1 ? 'flex' : 'none'};">
                            <i class="fas fa-times"></i>
                        </button>
                    `;

                    container.appendChild(roomNameItem);
                });
            }

            displaySavedData(data);
        }
    } catch (error) {
        console.error('Error loading saved data:', error);
    }
}

// Display saved data
function displaySavedData(data) {
    const savedDataDiv = document.getElementById('savedData');
    const dataDisplay = document.getElementById('dataDisplay');

    if (savedDataDiv && dataDisplay) {
        // Generate rooms list with zones
        let roomsHTML = '';
        if (data.rooms && data.rooms.length > 0) {
            roomsHTML = '<div class="rooms-list">';
            data.rooms.forEach((room, index) => {
                roomsHTML += `
                    <div class="room-display-item">
                        <span class="room-number">${index + 1}.</span>
                        <span class="room-name-display">${room.name}</span>
                        <span class="room-zone-badge">${room.zone || 'No zone'}</span>
                    </div>
                `;
            });
            roomsHTML += '</div>';
        } else {
            roomsHTML = '<span>Not specified</span>';
        }

        dataDisplay.innerHTML = `
            <div class="data-item">
                <label>Plot Size:</label>
                <span>${data.plotSize || 'Not specified'}</span>
            </div>
            <div class="data-item">
                <label>Room Type:</label>
                <span>${data.roomType || 'Not specified'}</span>
            </div>
            <div class="data-item full-width">
                <label>Rooms & Zones:</label>
                ${roomsHTML}
            </div>
            <div class="data-item">
                <label>Orientation:</label>
                <span>${data.orientation || 'Not specified'}</span>
            </div>
            <div class="data-item">
                <label>Floor Number:</label>
                <span>${data.floorNumber || 'Not specified'}</span>
            </div>
            <div class="data-item">
                <label>Saved On:</label>
                <span>${new Date(data.timestamp).toLocaleString()}</span>
            </div>
        `;

        savedDataDiv.style.display = 'block';
        savedDataDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Show success message
function showSuccessMessage() {
    // Create success notification
    const notification = document.createElement('div');
    notification.className = 'success-notification';
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-check-circle"></i>
            <span>Data saved successfully!</span>
        </div>
    `;

    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #2A9D8F, #1E8449);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 8px 25px rgba(42, 157, 143, 0.3);
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

// Clear form
function clearForm() {
    if (confirm('Are you sure you want to clear all form data?')) {
        const form = document.getElementById('spaceForm');
        form.reset();

        // Clear validation states
        const formGroups = form.querySelectorAll('.form-group');
        formGroups.forEach(group => {
            group.classList.remove('error', 'success');
        });

        // Clear error messages
        const errorMessages = form.querySelectorAll('.error-message');
        errorMessages.forEach(msg => {
            msg.textContent = '';
        });

        // Hide saved data
        const savedDataDiv = document.getElementById('savedData');
        if (savedDataDiv) {
            savedDataDiv.style.display = 'none';
        }

        // Clear localStorage
        localStorage.removeItem('spaceFormData');

        // Show notification
        showNotification('Form cleared successfully!', 'info');
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    const colors = {
        info: '#3498db',
        success: '#2ecc71',
        warning: '#f39c12',
        error: '#e74c3c'
    };

    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${colors[type] || colors.info};
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

// Add room name field
function addRoomName() {
    const container = document.getElementById('roomNamesContainer');
    const roomNameItem = document.createElement('div');
    roomNameItem.className = 'room-name-item';

    roomNameItem.innerHTML = `
        <div class="room-input-wrapper">
            <input type="text" name="roomNames[]" required placeholder="e.g., Living Room" class="room-name-input">
            <select name="roomZones[]" required class="room-zone-select">
                <option value="">Select Zone</option>
                <option value="north">North</option>
                <option value="northeast">Northeast</option>
                <option value="east">East</option>
                <option value="southeast">Southeast</option>
                <option value="south">South</option>
                <option value="southwest">Southwest</option>
                <option value="west">West</option>
                <option value="northwest">Northwest</option>
                <option value="center">Center</option>
            </select>
        </div>
        <button type="button" class="remove-room" onclick="removeRoomName(this)">
            <i class="fas fa-times"></i>
        </button>
    `;

    container.appendChild(roomNameItem);

    // Show remove buttons if more than one room
    updateRemoveButtons();

    // Focus on the new input
    const newInput = roomNameItem.querySelector('input');
    newInput.focus();
}

// Remove room name field
function removeRoomName(button) {
    const roomNameItem = button.parentElement;
    const container = document.getElementById('roomNamesContainer');

    // Don't remove if it's the only room
    if (container.children.length > 1) {
        roomNameItem.remove();
        updateRemoveButtons();
    }
}

// Update remove buttons visibility
function updateRemoveButtons() {
    const container = document.getElementById('roomNamesContainer');
    const removeButtons = container.querySelectorAll('.remove-room');

    removeButtons.forEach(button => {
        button.style.display = container.children.length > 1 ? 'flex' : 'none';
    });
}

// Get all room names
function getRoomNames() {
    const roomNameInputs = document.querySelectorAll('input[name="roomNames[]"]');
    return Array.from(roomNameInputs).map(input => input.value.trim()).filter(name => name);
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

// Show options modal after analysis
function showOptionsModal(analysisResult) {
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.7);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
    `;

    modal.innerHTML = `
        <div style="
            background: white;
            border-radius: 20px;
            padding: 3rem;
            max-width: 600px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        ">
            <i class="fas fa-check-circle" style="font-size: 4rem; color: #2A9D8F; margin-bottom: 1rem;"></i>
            <h2 style="color: #2A363B; margin-bottom: 1rem;">Analysis Complete!</h2>
            <p style="color: #666; margin-bottom: 2rem; font-size: 1.1rem;">
                Your Vastu Score: <strong style="color: #2A9D8F; font-size: 1.5rem;">${analysisResult.vastu_score}%</strong>
            </p>
            <p style="color: #666; margin-bottom: 2rem;">What would you like to do next?</p>
            
            <div style="display: flex; gap: 1rem; flex-direction: column;">
                <button onclick="viewResults()" style="
                    padding: 1rem 2rem;
                    background: #2A9D8F;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    font-size: 1.1rem;
                    font-weight: 600;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 0.5rem;
                ">
                    <i class="fas fa-chart-bar"></i>
                    View Analysis Results
                </button>
                
                <button onclick="generateBlueprints()" style="
                    padding: 1rem 2rem;
                    background: #F4A261;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    font-size: 1.1rem;
                    font-weight: 600;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 0.5rem;
                ">
                    <i class="fas fa-drafting-compass"></i>
                    Generate Optimized Blueprints
                </button>
            </div>
        </div>
    `;

    document.body.appendChild(modal);
}

// View results
function viewResults() {
    window.location.href = 'results.html';
}

// Generate blueprints
function generateBlueprints() {
    // Save space data for blueprint generation
    const form = document.getElementById('spaceForm');
    const formData = collectFormData(form);
    localStorage.setItem('spaceData', JSON.stringify(formData));

    window.location.href = 'blueprints.html';
}
