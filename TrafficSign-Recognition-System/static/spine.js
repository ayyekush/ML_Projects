// DOM Elements
const fileInput = document.getElementById('fileInput');
const imageUrl = document.getElementById('imageUrl');
const fetchUrlBtn = document.getElementById('fetchUrlBtn');
const randomCount = document.getElementById('randomCount');
const randomBtn = document.getElementById('randomBtn');
const resultsSection = document.getElementById('resultsSection');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultsGrid = document.getElementById('resultsGrid');
const cropModal = document.getElementById('cropModal');
const cropperImage = document.getElementById('cropperImage');
const closeCropModalBtn = document.getElementById('closeCropModal');
const cancelCropBtn = document.getElementById('cancelCropBtn');
const applyCropBtn = document.getElementById('applyCropBtn');

// Variables
let cropper;
let originalImage = null;
let currentImageSrc = null;

// Functions

// Function to open crop modal
function openCropModal(imageSrc) {
    currentImageSrc = imageSrc;
    cropperImage.src = imageSrc;
    cropModal.style.display = 'block';
    
    // Initialize cropper with the image
    if (cropper) {
        cropper.destroy();
    }
    
    setTimeout(() => {
        cropper = new Cropper(cropperImage, {
            aspectRatio: NaN, // Free aspect ratio
            viewMode: 1,
            movable: true,
            zoomable: true,
            rotatable: false
        });
    }, 100); // Small delay to ensure image is loaded
}

// Function to close crop modal
function closeCropModal() {
    cropModal.style.display = 'none';
    if (cropper) {
        cropper.destroy();
        cropper = null;
    }
}

async function predictUploadedImage(imageData) {
    resultsSection.style.display = 'block';
    loadingSpinner.style.display = 'block';
    resultsGrid.innerHTML = '';
    
    try {
        // Create a blob from the data URL
        const response = await fetch(imageData);
        const blob = await response.blob();
        
        // Create FormData and append the blob
        const formData = new FormData();
        formData.append('uploaded_Img', blob, 'image.jpg');
        
        const apiResponse = await fetch('/predict-uploaded-img', {
            method: 'POST',
            body: formData
        });
        
        if (!apiResponse.ok) {
            throw new Error('Failed to get prediction');
        }
        
        const data = await apiResponse.json();
        
        loadingSpinner.style.display = 'none';
        showPredictionResults([{
            image_base64: imageData,
            meta_image: `data:image/jpeg;base64,${data.base64_Meta_Img}`
        }]);
        
        resultsSection.scrollIntoView({ behavior: 'smooth' });
        
    } catch (error) {
        loadingSpinner.style.display = 'none';
        alert('Error getting prediction: ' + error.message);
    }
}

async function generateRandomPredictions() {
    const count = parseInt(randomCount.value);
    
    if (isNaN(count) || count < 1 || count > 30) {
        alert('Please enter a valid number between 1 and 30.');
        return;
    }
    
    resultsSection.style.display = 'block';
    loadingSpinner.style.display = 'block';
    resultsGrid.innerHTML = '';
    
    try {
        const response = await fetch(`/n-random-predictions?n=${count}`, {
            method: 'GET'
        });
        
        if (!response.ok) {
            throw new Error('Failed to get random predictions');
        }
        
        const data = await response.json();
        loadingSpinner.style.display = 'none';
        
        // Format the random prediction results
        const predictions = [];
        for(let i = 0; i < data.test_Img_List.length; i++) {
            predictions.push({
                image_base64: `data:image/jpeg;base64,${data.test_Img_List[i]}`,
                meta_image: `data:image/jpeg;base64,${data.pred_Meta_Img_List[i]}`
            });
        }
        
        showPredictionResults(predictions);
        resultsSection.scrollIntoView({ behavior: 'smooth' });
        
    } catch (error) {
        loadingSpinner.style.display = 'none';
        alert('Error getting random predictions: ' + error.message);
    }
}

function showPredictionResults(predictions) {
    resultsGrid.innerHTML = '';
    
    predictions.forEach(prediction => {
        const card = document.createElement('div');
        card.className = 'result-card';
        
        // Structure showing both original and predicted images side by side
        card.innerHTML = `
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
                <div style="flex: 1; padding: 5px;">
                    <img src="${prediction.image_base64}" alt="Original Image" style="max-width: 100%; height: auto;">
                    <p style="text-align: center; font-size: 0.9rem; margin-top: 5px;">Original</p>
                </div>
                <div style="flex: 1; padding: 5px;">
                    <img src="${prediction.meta_image}" alt="Best Match" style="max-width: 100%; height: auto;">
                    <p style="text-align: center; font-size: 0.9rem; margin-top: 5px;">Best Match</p>
                </div>
            </div>
            <div class="info">
                <h4>Traffic Sign Match</h4>
            </div>
        `;
        
        resultsGrid.appendChild(card);
    });
}

// URL handling functions

async function handleUrlImage() {
    const url = imageUrl.value.trim();
    if (!url) return;
    
    loadingSpinner.style.display = 'block';
    
    try {
        // For direct use of URLs, we need to make a proxy request to fetch the image
        // Since we can't modify app.py, we'll use a workaround
        const response = await fetch(url, { 
            method: 'GET',
            mode: 'cors'
        }).catch(() => {
            // If direct fetch fails, try our server as proxy
            return fetch('/predict-from-url', {
                method: 'POST',
                body: new FormData().append('url', url)
            });
        });
        
        // If we got a successful response and it's an image
        if (response.ok && response.headers.get('content-type').startsWith('image/')) {
            const blob = await response.blob();
            const reader = new FileReader();
            
            reader.onload = function(e) {
                // Open crop modal with the fetched image
                openCropModal(e.target.result);
                loadingSpinner.style.display = 'none';
            };
            
            reader.readAsDataURL(blob);
        } else {
            // Try to use our existing endpoint and extract just the image
            const formData = new FormData();
            formData.append('url', url);
            
            const apiResponse = await fetch('/predict-from-url', {
                method: 'POST',
                body: formData
            });
            
            if (!apiResponse.ok) {
                throw new Error('You have given wrong Address.\nYou must have been copying link to site, copy \"IMAGE ADDRESS\"');
            }
            
            // We'll have to use the URL directly in the cropper
            // This isn't ideal but should work for most cases
            openCropModal(url);
            loadingSpinner.style.display = 'none';
        }
        
    } catch (error) {
        loadingSpinner.style.display = 'none';
        alert('Error fetching image: ' + error.message);
    }
}

// Event Listeners

// File upload
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file || !file.type.startsWith('image/')) {
        alert('Please select a valid image file.');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = (e) => {
        originalImage = e.target.result;
        openCropModal(originalImage);
    };
    reader.readAsDataURL(file);
});

// URL fetch button
fetchUrlBtn.addEventListener('click', handleUrlImage);

// URL enter key handler
imageUrl.addEventListener('keyup', (e) => {
    if (e.key === 'Enter') handleUrlImage();
});

// Random button
randomBtn.addEventListener('click', generateRandomPredictions);

// Crop modal controls
closeCropModalBtn.addEventListener('click', closeCropModal);
cancelCropBtn.addEventListener('click', closeCropModal);

applyCropBtn.addEventListener('click', () => {
    if (!cropper) {
        alert('Please crop the image first.');
        return;
    }
    
    // Get cropped canvas and convert to base64
    const canvas = cropper.getCroppedCanvas({
        width: 200,  // Optional width
        height: 200, // Optional height
        imageSmoothingEnabled: true,
        imageSmoothingQuality: 'high'
    });
    
    const croppedImage = canvas.toDataURL('image/jpeg');
    
    // Close modal
    closeCropModal();
    
    // Now process the cropped image
    predictUploadedImage(croppedImage);
});

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    console.log('Traffic Sign Predictor ready');
});