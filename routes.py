import os
import uuid
import numpy as np
from flask import Blueprint, render_template, request, jsonify, current_app, url_for
from werkzeug.utils import secure_filename
from app.models.prediction import predict_image, get_model_details

# Create a blueprint
main_bp = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'dcm', 'nii', 'nii.gz'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_bp.route('/')
def index():
    model_details = get_model_details()
    return render_template('index.html', model_details=model_details)

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Create a unique filename
        file_ext = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_ext}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save the file
        file.save(filepath)
        
        # Process the image and get predictions
        try:
            results = predict_image(filepath)
            
            # Save the visualization if it exists
            vis_path = None
            if 'visualization' in results:
                vis_filename = f"vis_{unique_filename}"
                vis_path = os.path.join(current_app.config['UPLOAD_FOLDER'], vis_filename)
                results['visualization'].save(vis_path)
                results['visualization_url'] = url_for('static', filename=f'uploads/{vis_filename}')
                del results['visualization']
            
            # Add the image URL to the results
            results['image_url'] = url_for('static', filename=f'uploads/{unique_filename}')
            
            return jsonify(results)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'File type not allowed'}), 400