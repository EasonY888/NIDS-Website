# NIDS-Self-Trained: AI-Enhanced Network Security

This project is a full-stack **Network Intrusion Detection System (NIDS)** developed as a technical solution for network monitoring. It combines a self-trained machine learning model for attack classification with the Google Gemini AI API to provide intelligent, human-readable security summaries.

## 🚀 Key Features
- **Flow-Level Detection:** Classifies network traffic into 9 distinct attack categories using a local TensorFlow model.
- **AI-Powered Insights:** Integrates Google Gemini Pro to translate raw security logs and model probabilities into plain-English summaries.
- **Dynamic File Processing:** Allows users to upload CSV network log files for immediate local analysis.
- **Professional Dashboard:** A responsive UI featuring real-time feedback, CSV format reminders, and a streamlined chat interface.

## 🛠️ Technology Stack
- **Backend:** Django (Python)
- **Machine Learning:** TensorFlow, NumPy, Pandas
- **AI Integration:** Google Gemini Pro (Generative AI)
- **Frontend:** HTML5, JavaScript (ES6+), Bootstrap 5
- **Environment Management:** Python-Dotenv, Virtualenv

## ⚙️ Installation & Setup

To run this project locally, follow these steps:

### 1. Clone & Environment
```bash
git clone [https://github.com/EasonY888/NIDS-Website.git](https://github.com/EasonY888/NIDS-Website.git)
cd NIDS-self-trained
python -m venv my_env
# Windows
my_env\Scripts\activate  
# Mac/Linux
source my_env/bin/activate
2. Install Dependencies
Bash
pip install -r requirements.txt
3. API & Secret Configuration (Required)
The project requires a .env file in the root directory to manage sensitive credentials. Users must generate their own keys.

Create a file named .env in the root folder.

Generate a unique Django Secret Key by running:

Bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

Generate you genai api key by going to Gemini Studio and creating a project (default project created usually when you logged in) and copy the api key.
Add your keys to the .env file:

Plaintext
GEMINI_API_KEY=your_gemini_api_key_here
DJANGO_SECRET_KEY=your_generated_key_here
DEBUG=True

4. Database & Launch
Bash
python manage.py migrate
python manage.py runserver
📊 Expected Data Format
To ensure correct classification, uploaded CSV files must contain the following headers:
IPV4_SRC_ADDR, L4_SRC_PORT, IPV4_DST_ADDR, L4_DST_PORT, PROTOCOL, L7_PROTO, IN_BYTES, OUT_BYTES, IN_PKTS, OUT_PKTS, TCP_FLAGS, FLOW_DURATION_MILLISECONDS.

🔒 Security & Best Practices
Secret Management: Sensitive credentials are managed via environment variables. The .env file is excluded from Git to prevent leaks.

Git Integrity: The .gitignore is configured to exclude db.sqlite3, .env, and local virtual environments.

Modular Design: Separate Django applications handle core logic and AI processing for better maintainability.

📚 Dataset Source
The ML component is designed for features derived from the UNSW-NB15 NIDS datasets.
