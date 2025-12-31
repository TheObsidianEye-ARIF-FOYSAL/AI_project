// Get DOM elements
const uploadArea = document.getElementById('uploadArea');
const imageInput = document.getElementById('imageInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const removeFile = document.getElementById('removeFile');
const previewImage = document.getElementById('previewImage');
const predictBtn = document.getElementById('predictBtn');
const loader = document.getElementById('loader');
const result = document.getElementById('result');
const animalName = document.getElementById('animalName');
const confidence = document.getElementById('confidence');
const confidenceFill = document.getElementById('confidenceFill');
const errorDiv = document.getElementById('error');

let selectedFile = null;

// Click to upload
uploadArea.addEventListener('click', () => {
  imageInput.click();
});

// Drag and drop functionality
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
  
  const files = e.dataTransfer.files;
  if (files.length > 0) {
    handleFileSelect(files[0]);
  }
});

// File input change
imageInput.addEventListener('change', (e) => {
  if (e.target.files.length > 0) {
    handleFileSelect(e.target.files[0]);
  }
});

// Handle file selection
function handleFileSelect(file) {
  // Validate file type
  if (!file.type.startsWith('image/')) {
    showError('Please upload a valid image file');
    return;
  }

  selectedFile = file;
  
  // Show file info
  fileName.textContent = file.name;
  fileInfo.classList.add('show');
  
  // Show preview
  const reader = new FileReader();
  reader.onload = (e) => {
    previewImage.src = e.target.result;
    previewImage.classList.add('show');
  };
  reader.readAsDataURL(file);
  
  // Show predict button
  predictBtn.classList.add('show');
  
  // Hide previous results
  result.classList.remove('show');
  errorDiv.classList.remove('show');
}

// Remove file
removeFile.addEventListener('click', (e) => {
  e.stopPropagation();
  clearSelection();
});

function clearSelection() {
  selectedFile = null;
  imageInput.value = '';
  fileInfo.classList.remove('show');
  previewImage.classList.remove('show');
  predictBtn.classList.remove('show');
  result.classList.remove('show');
  errorDiv.classList.remove('show');
}

// Predict button click
predictBtn.addEventListener('click', uploadImage);

// Upload and predict
async function uploadImage() {
  if (!selectedFile) {
    showError('Please select an image first');
    return;
  }

  // Show loader
  loader.classList.add('show');
  predictBtn.disabled = true;
  result.classList.remove('show');
  errorDiv.classList.remove('show');

  const formData = new FormData();
  formData.append('file', selectedFile);

  try {
    // Use relative URL for same-origin requests, or full URL for Render
    const apiUrl = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
      ? '/predict'  // Local development
      : '/predict'; // Production (same origin)

    const response = await fetch(apiUrl, {
      method: 'POST',
      body: formData
    });

    // Check if response is ok before trying to parse JSON
    if (!response.ok) {
      // Try to get error message, but handle empty responses
      let errorMsg = `Server error (${response.status})`;
      try {
        const data = await response.json();
        errorMsg = data.error || data.message || errorMsg;
      } catch (e) {
        // Response body is empty or not JSON
        if (response.status === 502) {
          errorMsg = 'Server is overloaded or crashed. The model might be too large for the free tier. Try again in a moment.';
        } else if (response.status === 503) {
          errorMsg = 'Service unavailable. Server is starting up, please wait 30 seconds and try again.';
        } else if (response.status === 504) {
          errorMsg = 'Request timeout. Prediction took too long. Server might need more resources.';
        }
      }
      showError(errorMsg);
      return;
    }

    const data = await response.json();

    if (response.ok) {
      showResult(data.prediction, data.confidence);
    } else {
      // Check if it's a 503 (service unavailable - model loading)
      if (response.status === 503 && data.model_loading) {
        showError('Model is loading. Please wait a moment and try again.');
      } else {
        showError(data.error || 'Prediction failed');
      }
    }
  } catch (error) {
    console.error('Error:', error);
    console.error('Error details:', {
      message: error.message,
      name: error.name,
      stack: error.stack
    });
    
    // More specific error messages
    let errorMessage = 'Network error. ';
    if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
      errorMessage += 'Cannot connect to server. Server may be down or starting up. ';
    } else if (error.message.includes('NetworkError')) {
      errorMessage += 'Network connection failed. ';
    }
    errorMessage += 'Please wait a moment and try again.';
    
    showError(errorMessage);
  } finally {
    loader.classList.remove('show');
    predictBtn.disabled = false;
  }
}

// Show result
function showResult(animal, conf) {
  animalName.textContent = animal;
  confidence.textContent = conf;
  
  // Animate confidence bar
  setTimeout(() => {
    confidenceFill.style.width = conf + '%';
  }, 100);
  
  result.classList.add('show');
  
  // Add emoji based on animal
  const animalEmojis = {
    'cat': '🐱',
    'dog': '🐶',
    'horse': '🐴',
    'sheep': '🐑',
    'cow': '🐄',
    'elephant': '🐘',
    'butterfly': '🦋',
    'chicken': '🐔',
    'spider': '🕷️',
    'squirrel': '🐿️'
  };
  
  const emoji = animalEmojis[animal.toLowerCase()] || '🐾';
  animalName.textContent = emoji + ' ' + animal;
}

// Show error
function showError(message) {
  errorDiv.textContent = '⚠️ ' + message;
  errorDiv.classList.add('show');
  
  setTimeout(() => {
    errorDiv.classList.remove('show');
  }, 5000);
}

// Prevent default drag behavior on the whole page
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
  document.body.addEventListener(eventName, (e) => {
    e.preventDefault();
    e.stopPropagation();
  });
});
