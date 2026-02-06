// Home page JavaScript for handling file uploads and analysis

document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const uploadPreview = document.getElementById('upload-preview');
    const previewImage = document.getElementById('preview-image');
    const changeImageBtn = document.getElementById('change-image-btn');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultsContainer = document.getElementById('results-container');
    const loadingIndicator = document.getElementById('loading-indicator');
    const resultsContent = document.getElementById('results-content');
    const resultOriginal = document.getElementById('result-original');
    const resultHeatmap = document.getElementById('result-heatmap');
    const resultClass = document.getElementById('result-class');
    const resultConfidence = document.getElementById('result-confidence');
    const resultTime = document.getElementById('result-time');
    const confidenceChart = document.getElementById('confidence-chart');
    const newAnalysisBtn = document.getElementById('new-analysis-btn');
    
    // Selected file for upload
    let selectedFile = null;
    
    // Add event listeners for file upload
    if (uploadArea) {
        uploadArea.addEventListener('click', () => fileInput.click());
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            
            if (e.dataTransfer.files.length) {
                handleFileSelect(e.dataTransfer.files[0]);
            }
        });
    }
    
    // File input change handler
    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length) {
                handleFileSelect(e.target.files[0]);
            }
        });
    }
    
    // Change image button handler
    if (changeImageBtn) {
        changeImageBtn.addEventListener('click', () => {
            selectedFile = null;
            uploadPreview.style.display = 'none';
            uploadArea.style.display = 'block';
        });
    }
    
    // Analyze button handler
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', () => {
            if (selectedFile) {
                analyzeImage(selectedFile);
            }
        });
    }
    
    // New analysis button handler
    if (newAnalysisBtn) {
        newAnalysisBtn.addEventListener('click', () => {
            selectedFile = null;
            resultsContainer.style.display = 'none';
            uploadPreview.style.display = 'none';
            uploadArea.style.display = 'block';
        });
    }
    
    // Handle file selection
    function handleFileSelect(file) {
        const allowedTypes = ['image/jpeg', 'image/png', 'image/dicom', 'application/dicom'];
        const fileExtension = file.name.split('.').pop().toLowerCase();
        
        // Check if file type is allowed
        if (!allowedTypes.includes(file.type) && 
            !['dcm', 'nii', 'nii.gz'].includes(fileExtension)) {
            alert('Please select a valid medical image file (JPEG, PNG, DICOM, or NIfTI)');
            return;
        }
        
        selectedFile = file;
        
        // Show preview if it's a standard image format
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            
            reader.onload = (e) => {
                previewImage.src = e.target.result;
                uploadArea.style.display = 'none';
                uploadPreview.style.display = 'block';
            };
            
            reader.readAsDataURL(file);
        } else {
            // For DICOM and NIfTI files, show a placeholder
            previewImage.src = '/static/images/dicom-placeholder.png';
            uploadArea.style.display = 'none';
            uploadPreview.style.display = 'block';
        }
    }
    
    // Analyze the image using the backend API
    function analyzeImage(file) {
        // Show loading indicator
        resultsContainer.style.display = 'block';
        loadingIndicator.style.display = 'flex';
        resultsContent.style.display = 'none';
        
        // Create form data for file upload
        const formData = new FormData();
        formData.append('file', file);
        
        // Send file to backend for analysis
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error analyzing image');
            }
            return response.json();
        })
        .then(data => {
            // Hide loading indicator and show results
            loadingIndicator.style.display = 'none';
            resultsContent.style.display = 'block';
            
            // Populate results
            resultOriginal.src = data.image_url;
            resultHeatmap.src = data.visualization_url;
            resultClass.textContent = data.class_name;
            resultConfidence.textContent = `${(data.confidence * 100).toFixed(1)}%`;
            resultTime.textContent = data.processing_time;
            
            // Create confidence bars
            createConfidenceBars(data.all_classes);
            
            // Scroll to results
            resultsContainer.scrollIntoView({ behavior: 'smooth' });
        })
        .catch(error => {
            console.error('Error:', error);
            loadingIndicator.style.display = 'none';
            alert('An error occurred while analyzing the image. Please try again.');
        });
    }
    
    // Create confidence bars for class probabilities
    function createConfidenceBars(classScores) {
        if (!confidenceChart) return;
        
        confidenceChart.innerHTML = '';
        
        // Create a bar for each class
        Object.entries(classScores).forEach(([className, score]) => {
            const percentage = (score * 100).toFixed(1);
            
            // Create the bar container
            const barContainer = document.createElement('div');
            barContainer.className = 'confidence-bar';
            
            // Create the fill
            const fill = document.createElement('div');
            fill.className = 'confidence-fill';
            fill.style.width = '0%'; // Start at 0 for animation
            
            // Create the label
            const label = document.createElement('div');
            label.className = 'confidence-label';
            label.textContent = className;
            
            // Create the value
            const value = document.createElement('div');
            value.className = 'confidence-value';
            value.textContent = `${percentage}%`;
            
            // Add elements to the bar
            barContainer.appendChild(fill);
            barContainer.appendChild(label);
            barContainer.appendChild(value);
            
            // Add the bar to the chart
            confidenceChart.appendChild(barContainer);
            
            // Animate the fill width after a short delay
            setTimeout(() => {
                fill.style.width = `${percentage}%`;
            }, 100);
        });
    }
}); 