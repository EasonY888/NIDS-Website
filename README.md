# NIDS Self-Trained Attack Detection System

This project is a local web-based Network Intrusion Detection System (NIDS)
that uses a self-trained machine learning model to classify network attacks
based on flow-level features.

## Features
- Upload CSV network log files
- Predict probabilities for 9 attack categories
- Local FastAPI backend
- Simple HTML frontend
- Designed for learning ML + cybersecurity

## Tech Stack
- Python
- FastAPI
- TensorFlow
- HTML / JavaScript

## Model Files
Trained models are not included in this repository.

To use the system:
1. Train the model locally using provided scripts
2. Place the model file in the `/model` directory
3. Run the backend server

This mirrors real-world ML deployment practices.

https://staff.itee.uq.edu.au/marius/NIDS_datasets/

NIDS-Self-Trained: AI-Enhanced Network Security
A full-stack web application developed to monitor network traffic patterns and provide intelligent security summaries using the Google Gemini AI API. This project demonstrates the integration of cybersecurity principles with modern web development.

🚀 Key Features
Traffic Analysis: Monitors incoming network data for potential intrusion patterns.

AI-Powered Insights: Uses LLMs to translate raw security logs into human-readable summaries.

Django Backend: Robust data management and user authentication.

Responsive UI: Styled with Bootstrap for a clean, professional dashboard experience.

🛠️ Technology Stack
Framework: Django (Python)

AI Integration: Google Gemini Pro (Generative AI)

Frontend: HTML5, CSS3, Bootstrap 5

Environment Management: Python-Dotenv, Virtualenv

⚙️ Installation & Setup
To run this project locally at Toronto Metropolitan University or on your own machine, follow these steps:

1. Clone & Environment
Bash
git clone https://github.com/HarshalPatelDev/NIDS-self-trained.git
cd NIDS-self-trained
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
2. Install Dependencies
Bash
pip install -r requirements.txt
3. API Configuration (Required)
This project requires a Gemini API key. Create a .env file in the root directory:

Plaintext
GEMINI_API_KEY=your_api_key_here
Note: The .env file is ignored by Git to ensure your personal API keys are never exposed publicly.

4. Database & Launch
Bash
python manage.py migrate
python manage.py runserver
🔒 Security & Best Practices
Secret Management: Sensitive credentials are managed via environment variables.

Git Integrity: .gitignore is configured to exclude db.sqlite3 and .env files.

Modular Design: Separate Django apps for core logic and AI processing.