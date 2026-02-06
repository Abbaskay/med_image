import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import io
import os
import time

# Global variable to store the model
model = None

# Class names for sample model
CLASS_NAMES = ['Normal', 'Tumor']

def load_model():
    """
    Load or create a model for medical image analysis.
    For demonstration, we'll create a simple CNN model that could be replaced with a pre-trained one.
    """
    global model
    
    if model is not None:
        return model
    
    # Simple CNN model for binary classification (normal vs abnormal)
    model = keras.Sequential([
        keras.layers.InputLayer(input_shape=(224, 224, 3)),
        keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
        keras.layers.MaxPooling2D(pool_size=(2, 2)),
        keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
        keras.layers.MaxPooling2D(pool_size=(2, 2)),
        keras.layers.Conv2D(128, kernel_size=(3, 3), activation='relu'),
        keras.layers.MaxPooling2D(pool_size=(2, 2)),
        keras.layers.Flatten(),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(2, activation='softmax')  # Binary classification
    ])
    
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    
    return model

def preprocess_image(image_path):
    """
    Preprocess the image for model input.
    Handles different medical image formats.
    """
    # Check file extension
    ext = os.path.splitext(image_path)[1].lower()
    
    if ext in ['.dcm']:
        # For DICOM files (would require pydicom in a real implementation)
        # This is a simplified version; in reality, you'd use pydicom
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        # Convert to 3 channels
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    elif ext in ['.nii', '.gz']:
        # For NIfTI files (would require nibabel in a real implementation)
        # This is a simplified version; in reality, you'd use nibabel
        img = cv2.imread(image_path)
        if img is None:
            img = np.zeros((224, 224, 3), dtype=np.uint8)
    else:
        # For regular image formats
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Resize to model input size
    img = cv2.resize(img, (224, 224))
    
    # Normalize pixel values
    img = img / 255.0
    
    return img

def generate_heatmap(img, model):
    """
    Generate a heatmap to visualize which regions the model focuses on.
    Using Grad-CAM technique (simplified version).
    """
    # Create a visualization of which pixels are important
    # This is a simplified version - in a real app, you would implement Grad-CAM or similar
    
    # Convert back to 0-255 range for visualization
    img_display = (img * 255).astype(np.uint8)
    
    # Create a simple heatmap (this is just for visualization)
    # In a real app, this would be based on model attention
    heatmap = cv2.applyColorMap(
        cv2.GaussianBlur(
            cv2.resize(
                np.random.randint(100, 200, size=(28, 28), dtype=np.uint8),
                (224, 224)
            ),
            (15, 15), 0
        ),
        cv2.COLORMAP_JET
    )
    
    # Overlay the heatmap on the image
    overlay = cv2.addWeighted(img_display, 0.7, heatmap, 0.3, 0)
    
    # Convert to PIL Image
    overlay_pil = Image.fromarray(overlay)
    
    return overlay_pil

def predict_image(image_path):
    """
    Make predictions on a medical image and return results.
    """
    # Load model
    model = load_model()
    
    # Preprocess image
    img = preprocess_image(image_path)
    
    # Simulate model prediction
    # In a real application, you would use model.predict()
    batch_img = np.expand_dims(img, axis=0)
    
    # For demo purposes, we'll simulate prediction
    # In a real scenario, you'd use: predictions = model.predict(batch_img)
    start_time = time.time()
    time.sleep(1)  # Simulate processing time
    
    # Simulate prediction scores (normally from model.predict())
    # This is just for demo - replace with actual model predictions in production
    prediction_scores = np.array([[0.15, 0.85]])  # Example: 85% probability of tumor
    
    # Generate a heatmap for visualization
    heatmap_img = generate_heatmap(img, model)
    
    # Get the class with highest probability
    predicted_class = np.argmax(prediction_scores, axis=1)[0]
    
    # Return the results
    results = {
        'class_name': CLASS_NAMES[predicted_class],
        'confidence': float(prediction_scores[0][predicted_class]),
        'all_classes': {CLASS_NAMES[i]: float(score) for i, score in enumerate(prediction_scores[0])},
        'processing_time': f"{time.time() - start_time:.2f}s",
        'visualization': heatmap_img
    }
    
    return results

def get_model_details():
    """Return details about the model for display in the UI."""
    return {
        'name': 'MedNet CNN',
        'type': 'Convolutional Neural Network',
        'target': 'Brain Tumor Detection',
        'classes': CLASS_NAMES,
        'input_size': '224x224 pixels',
        'description': 'A deep learning model designed to detect abnormalities in brain MRI scans.'
    } 