// Dashboard JavaScript

document.addEventListener('DOMContentLoaded', function () {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const uploadedFiles = document.getElementById('uploadedFiles');
    const filesList = document.getElementById('filesList');
    const analysisResults = document.getElementById('analysisResults');

    let uploadedFilesList = [];

    // Initialize dashboard
    initializeDashboard();

    // Upload area click handler
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    // File input change handler
    fileInput.addEventListener('change', handleFileSelect);

    // Drag and drop handlers
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);

    // Analyze button handler
    analyzeBtn.addEventListener('click', analyzeFloorPlan);

    // Space button handler
    const spaceBtn = document.getElementById('spaceBtn');
    if (spaceBtn) {
        spaceBtn.addEventListener('click', createNewSpace);
    }
});

// Initialize dashboard
function initializeDashboard() {
    // Clear any existing data
    uploadedFilesList = [];
    updateUI();
}

// Handle file selection
function handleFileSelect(event) {
    const files = Array.from(event.target.files);
    processFiles(files);
}

// Handle drag over
function handleDragOver(event) {
    event.preventDefault();
    event.currentTarget.classList.add('dragover');
}

// Handle drag leave
function handleDragLeave(event) {
    event.currentTarget.classList.remove('dragover');
}

// Handle drop
function handleDrop(event) {
    event.preventDefault();
    event.currentTarget.classList.remove('dragover');

    const files = Array.from(event.dataTransfer.files);
    processFiles(files);
}

// Process uploaded files
function processFiles(files) {
    files.forEach(file => {
        if (validateFile(file)) {
            uploadedFilesList.push({
                id: Date.now() + Math.random(),
                file: file,
                name: file.name,
                size: formatFileSize(file.size),
                type: file.type,
                uploadTime: new Date()
            });
        }
    });

    updateUI();
}

// Validate file
function validateFile(file) {
    const maxSize = 5 * 1024 * 1024; // 5MB
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'application/pdf'];

    if (file.size > maxSize) {
        showNotification('File size must be less than 5MB', 'error');
        return false;
    }

    if (!allowedTypes.includes(file.type)) {
        showNotification('Only JPG, PNG, and PDF files are allowed', 'error');
        return false;
    }

    return true;
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Update UI
function updateUI() {
    updateUploadedFiles();
    updateAnalyzeButton();
}

// Update uploaded files display
function updateUploadedFiles() {
    if (uploadedFilesList.length === 0) {
        uploadedFiles.style.display = 'none';
        return;
    }

    uploadedFiles.style.display = 'block';
    filesList.innerHTML = '';

    uploadedFilesList.forEach(fileItem => {
        const fileElement = createFileElement(fileItem);
        filesList.appendChild(fileElement);
    });
}

// Create file element
function createFileElement(fileItem) {
    const fileElement = document.createElement('div');
    fileElement.className = 'file-item';
    fileElement.innerHTML = `
        <div class="file-icon">
            <i class="${getFileIcon(fileItem.type)}"></i>
        </div>
        <div class="file-info">
            <div class="file-name">${fileItem.name}</div>
            <div class="file-size">${fileItem.size}</div>
        </div>
        <div class="file-actions">
            <button class="file-action" onclick="previewFile('${fileItem.id}')" title="Preview">
                <i class="fas fa-eye"></i>
            </button>
            <button class="file-action" onclick="removeFile('${fileItem.id}')" title="Remove">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    `;

    return fileElement;
}

// Get file icon based on type
function getFileIcon(type) {
    if (type.includes('image')) {
        return 'fas fa-image';
    } else if (type.includes('pdf')) {
        return 'fas fa-file-pdf';
    } else {
        return 'fas fa-file';
    }
}

// Preview file
function previewFile(fileId) {
    const fileItem = uploadedFilesList.find(item => item.id == fileId);
    if (fileItem) {
        const url = URL.createObjectURL(fileItem.file);
        window.open(url, '_blank');
    }
}

// Remove file
function removeFile(fileId) {
    uploadedFilesList = uploadedFilesList.filter(item => item.id != fileId);
    updateUI();
    showNotification('File removed successfully', 'success');
}

// Update analyze button
function updateAnalyzeButton() {
    const analyzeBtn = document.getElementById('analyzeBtn');

    if (uploadedFilesList.length > 0) {
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = `
            <i class="fas fa-search"></i>
            Analyze My Floor Plan (${uploadedFilesList.length} file${uploadedFilesList.length > 1 ? 's' : ''})
        `;
    } else {
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = `
            <i class="fas fa-search"></i>
            Analyze My Floor Plan
        `;
    }
}

// Analyze floor plan
async function analyzeFloorPlan() {
    if (uploadedFilesList.length === 0) {
        showNotification('Please upload at least one file', 'error');
        return;
    }

    const analyzeBtn = document.getElementById('analyzeBtn');
    const analysisResults = document.getElementById('analysisResults');
    const file = uploadedFilesList[0].file;

    // Show loading state
    analyzeBtn.classList.add('loading');
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';

    try {
        // Convert to Base64
        const base64Image = await new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = error => reject(error);
            reader.readAsDataURL(file);
        });

        // Call Python Backend (Port 5001)
        const response = await fetch('http://localhost:5001/analyze_image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                image: base64Image,
                filename: file.name
            })
        });

        const data = await response.json();

        if (data.success) {
            // Update UI with REAL data from Python
            updateAnalysisResults(data);

            showNotification('Analysis completed successfully!', 'success');

            // Show results
            analysisResults.style.display = 'block';
            analysisResults.scrollIntoView({ behavior: 'smooth' });
        } else {
            throw new Error(data.error || 'Analysis failed');
        }

    } catch (error) {
        console.error('Analysis Error:', error);
        showNotification('Analysis failed: ' + error.message, 'error');
    } finally {
        analyzeBtn.classList.remove('loading');
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = '<i class="fas fa-search"></i> Analyze My Floor Plan';
    }
}

function updateAnalysisResults(data) {
    document.getElementById('vastuScoreDisplay').innerText = data.vastu_score + "%";
    document.getElementById('mlScoreDisplay').innerText = "ML: " + data.ml_score;
    document.getElementById('ruleScoreDisplay').innerText = "Rules: " + data.rule_score;

    // 2D Viz
    if (data.visualization) {
        document.getElementById('visualizationImage').src = "data:image/png;base64," + data.visualization;
    }

    // Recommendations
    const recContainer = document.getElementById('recommendationsContainer');
    recContainer.innerHTML = '';
    data.recommendations.forEach(rec => {
        const div = document.createElement('div');
        div.className = 'result-item';
        div.innerHTML = `
            <i class="fas fa-exclamation-triangle" style="color:${rec.score > 70 ? 'green' : 'orange'}"></i>
            <div>
                <h4>${rec.element} Element (${rec.score}%)</h4>
                <p>${rec.message}</p>
            </div>
        `;
        recContainer.appendChild(div);
    });

    // Elements Breakdown
    const elContainer = document.getElementById('elementsBreakdown');
    elContainer.innerHTML = '';
    for (const [key, value] of Object.entries(data.elements)) {
        const div = document.createElement('div');
        div.style.textAlign = 'center';
        div.innerHTML = `
             <div style="font-weight:bold; color:#555;">${key}</div>
             <div style="font-size:1.5rem; color:var(--primary);">${value}%</div>
        `;
        elContainer.appendChild(div);
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;

    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#2A9D8F' : type === 'error' ? '#ff4757' : '#3498db'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        animation: slideInRight 0.3s ease;
        max-width: 400px;
    `;

    document.body.appendChild(notification);

    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Keyboard shortcuts
document.addEventListener('keydown', function (e) {
    // Ctrl/Cmd + O to open file dialog
    if ((e.ctrlKey || e.metaKey) && e.key === 'o') {
        e.preventDefault();
        document.getElementById('fileInput').click();
    }

    // Escape to clear selection
    if (e.key === 'Escape') {
        clearSelection();
    }
});

// Clear selection
function clearSelection() {
    uploadedFilesList = [];
    updateUI();
    document.getElementById('analysisResults').style.display = 'none';
}

// File upload progress (for future implementation)
function showUploadProgress(fileId, progress) {
    const fileElement = document.querySelector(`[data-file-id="${fileId}"]`);
    if (fileElement) {
        const progressBar = fileElement.querySelector('.progress-bar');
        if (progressBar) {
            progressBar.style.width = `${progress}%`;
        }
    }
}

// Export functionality (for future implementation)
function exportResults() {
    const results = {
        files: uploadedFilesList.map(item => ({
            name: item.name,
            size: item.size,
            type: item.type,
            uploadTime: item.uploadTime
        })),
        analysisTime: new Date().toISOString()
    };

    const dataStr = JSON.stringify(results, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });

    const link = document.createElement('a');
    link.href = URL.createObjectURL(dataBlob);
    link.download = 'vastu-analysis-results.json';
    link.click();
}

// Initialize tooltips
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[title]');
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

// Show tooltip
function showTooltip(event) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = event.target.title;
    tooltip.style.cssText = `
        position: absolute;
        background: var(--neutral);
        color: white;
        padding: 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        z-index: 1000;
        pointer-events: none;
    `;

    document.body.appendChild(tooltip);

    const rect = event.target.getBoundingClientRect();
    tooltip.style.left = rect.left + 'px';
    tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';

    event.target._tooltip = tooltip;
}

// Hide tooltip
function hideTooltip(event) {
    if (event.target._tooltip) {
        event.target._tooltip.remove();
        delete event.target._tooltip;
    }
}

// Initialize tooltips on page load
document.addEventListener('DOMContentLoaded', initializeTooltips);

// Create new space functionality
function createNewSpace() {
    // Show space creation modal
    showSpaceModal();
}

// Show space creation modal
function showSpaceModal() {
    const modal = document.createElement('div');
    modal.className = 'space-modal';
    modal.innerHTML = `
        <div class="space-modal-content">
            <div class="space-modal-header">
                <h3><i class="fas fa-plus"></i> Create New Space</h3>
                <button class="close-modal" onclick="closeSpaceModal()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="space-modal-body">
                <div class="form-group">
                    <label for="spaceName">Space Name *</label>
                    <input type="text" id="spaceName" placeholder="e.g., Living Room, Bedroom, Kitchen">
                </div>
                <div class="form-group">
                    <label for="spaceType">Space Type *</label>
                    <select id="spaceType">
                        <option value="">Select Space Type</option>
                        <option value="living-room">Living Room</option>
                        <option value="bedroom">Bedroom</option>
                        <option value="kitchen">Kitchen</option>
                        <option value="bathroom">Bathroom</option>
                        <option value="office">Office</option>
                        <option value="dining-room">Dining Room</option>
                        <option value="puja-room">Puja Room</option>
                        <option value="other">Other</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="spaceDimensions">Dimensions (Optional)</label>
                    <input type="text" id="spaceDimensions" placeholder="e.g., 12ft x 10ft">
                </div>
                <div class="form-group">
                    <label for="spaceDescription">Description (Optional)</label>
                    <textarea id="spaceDescription" placeholder="Describe your space..."></textarea>
                </div>
            </div>
            <div class="space-modal-footer">
                <button class="btn-cancel" onclick="closeSpaceModal()">Cancel</button>
                <button class="btn-create" onclick="saveNewSpace()">Create Space</button>
            </div>
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

    const modalContent = modal.querySelector('.space-modal-content');
    modalContent.style.cssText = `
        background: white;
        border-radius: 20px;
        padding: 2rem;
        max-width: 500px;
        width: 90%;
        max-height: 80vh;
        overflow-y: auto;
        animation: slideUp 0.3s ease;
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
        .space-modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid #f0f0f0;
        }
        .space-modal-header h3 {
            color: var(--neutral);
            margin: 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .close-modal {
            background: none;
            border: none;
            font-size: 1.5rem;
            color: var(--muted-gray);
            cursor: pointer;
            padding: 0.5rem;
            border-radius: 50%;
            transition: all 0.3s ease;
        }
        .close-modal:hover {
            background: #f0f0f0;
            color: var(--neutral);
        }
        .space-modal-body {
            margin-bottom: 2rem;
        }
        .space-modal-body .form-group {
            margin-bottom: 1.5rem;
        }
        .space-modal-body label {
            display: block;
            font-weight: 600;
            color: var(--neutral);
            margin-bottom: 0.5rem;
        }
        .space-modal-body input,
        .space-modal-body select,
        .space-modal-body textarea {
            width: 100%;
            padding: 1rem;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        .space-modal-body input:focus,
        .space-modal-body select:focus,
        .space-modal-body textarea:focus {
            outline: none;
            border-color: var(--primary);
        }
        .space-modal-body textarea {
            resize: vertical;
            min-height: 80px;
        }
        .space-modal-footer {
            display: flex;
            gap: 1rem;
            justify-content: flex-end;
        }
        .btn-cancel, .btn-create {
            padding: 1rem 2rem;
            border-radius: 10px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .btn-cancel {
            background: #f0f0f0;
            color: var(--neutral);
            border: none;
        }
        .btn-cancel:hover {
            background: #e0e0e0;
        }
        .btn-create {
            background: var(--primary);
            color: white;
            border: none;
        }
        .btn-create:hover {
            background: var(--accent);
            transform: translateY(-2px);
        }
    `;
    document.head.appendChild(style);
}

// Close space modal
function closeSpaceModal() {
    const modal = document.querySelector('.space-modal');
    if (modal) {
        modal.remove();
    }
}

// Save new space
function saveNewSpace() {
    const spaceName = document.getElementById('spaceName').value;
    const spaceType = document.getElementById('spaceType').value;
    const spaceDimensions = document.getElementById('spaceDimensions').value;
    const spaceDescription = document.getElementById('spaceDescription').value;

    if (!spaceName || !spaceType) {
        showNotification('Please fill in all required fields', 'error');
        return;
    }

    // Create space object
    const newSpace = {
        id: Date.now(),
        name: spaceName,
        type: spaceType,
        dimensions: spaceDimensions,
        description: spaceDescription,
        createdAt: new Date().toISOString()
    };

    // Save to localStorage (in real app, this would be sent to server)
    const spaces = JSON.parse(localStorage.getItem('vastuSpaces') || '[]');
    spaces.push(newSpace);
    localStorage.setItem('vastuSpaces', JSON.stringify(spaces));

    // Close modal and show success
    closeSpaceModal();
    showNotification('Space created successfully!', 'success');

    // Update UI if needed
    updateSpacesList();
}

// Update spaces list (if you have a spaces list on the page)
function updateSpacesList() {
    // This function can be used to update any spaces list on the page
    console.log('Spaces list updated');
}

// Helper for 'Analyze Another' button
function analyzeAnother() {
    clearSelection();
    document.getElementById('fileInput').value = '';
}

