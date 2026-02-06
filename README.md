# MedImage AI - Medical Image Analysis

An advanced web application for analyzing medical images using deep learning. This tool assists in identifying abnormalities such as tumors in medical images like MRI and CT scans.

## Technologies Used

- **TensorFlow/Keras**: Deep learning framework for building and training neural networks
- **OpenCV**: Computer vision library for image processing
- **Flask**: Web framework for the application backend
- **JavaScript/HTML/CSS**: Frontend implementation

## Features

- Upload medical images for analysis (JPEG, PNG, DICOM, NIfTI formats)
- Deep learning-based analysis for abnormality detection
- Visualization of results with heatmaps showing regions of interest
- Detailed analysis report with confidence scores and predictions

## Installation

1. Clone this repository:
```
git clone <repository-url>
cd med_image
```

2. Create a virtual environment (recommended):
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

## Running the Application

Start the Flask server:
```
python app.py
```

The application will be available at http://localhost:5000

## Project Structure

```
med_image/
├── app/
│   ├── __init__.py         # Flask application initialization
│   ├── routes.py           # Web routes and API endpoints
│   ├── models/             # ML models and prediction logic
│   │   └── prediction.py   # Image analysis implementation
│   ├── static/             # Static files (CSS, JS, images)
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/          # HTML templates
│       ├── base.html
│       ├── index.html
│       └── about.html
├── app.py                  # Main application entry point
└── requirements.txt        # Project dependencies
```

## Important Note

This tool is intended to assist medical professionals and should not be used as a replacement for professional medical diagnosis. Always consult with a qualified healthcare provider for medical advice. 