# 🧠 NeuroNet
## AI Assistant for Detecting and Managing Paralysis in Patients

NeuroNet is a web-based AI-powered medical assistance system designed to support the early detection of facial and speech paralysis. The application analyzes facial images and voice recordings using Artificial Intelligence and provides preliminary medical insights along with an interactive medical chatbot.

> ⚠️ Disclaimer: This application is intended only for preliminary screening and does not replace professional medical diagnosis.

---

## 📌 Project Overview

Early diagnosis of neurological disorders such as Bell’s palsy, facial paralysis, stroke-related paralysis, and dysarthria plays a crucial role in improving patient recovery outcomes. NeuroNet bridges the accessibility gap by providing an AI-driven, web-based screening tool that can be accessed anytime and anywhere.

The system is developed using the Flask framework and integrates OpenRouter’s LLaMA-3.1 Large Language Model to generate meaningful medical interpretations.

---

## 🚀 Key Features

- Facial paralysis detection from uploaded images  
- Speech paralysis detection using voice recordings  
- AI-based medical analysis using OpenRouter (LLaMA-3.1)  
- Secure user authentication (Login and Registration)  
- Interactive paralysis-focused medical chatbot  
- Image and audio preprocessing for reliable analysis  
- Responsive and user-friendly web interface  
- Secure session handling and data privacy  

---

## 🛠️ Technology Stack

### Backend
- Python 3.8+
- Flask
- Requests
- Pillow (PIL)
- Base64 Encoding

### Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap 5
- Jinja2 Templates

### AI & API
- OpenRouter API
- LLaMA-3.1-8B Large Language Model

---

## 🏗️ System Architecture

1. User Authentication  
2. Image / Voice Upload  
3. Preprocessing (Crop, Resize, Encode)  
4. AI Analysis via OpenRouter API  
5. Result Visualization  
6. Chatbot Interaction  
7. Session Management  

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Stable internet connection
- OpenRouter API key

### Clone the Repository
git clone https://github.com/your-username/NeuroNet.git
cd NeuroNet

### Create Virtual Environment
pip install virtualenv
virtualenv paralysis_env

### Activate Environment

**Windows**
paralysis_env\Scripts\activate

**Linux / macOS**
source paralysis_env/bin/activate

### Install Dependencies
pip install -r requirements.txt

---

## 🔑 API Configuration

Add your OpenRouter API key in `app.py` or a `.env` file:

OPENROUTER_API_KEY = "your_api_key_here"

Keep your API key private and secure.

---

## ▶️ Running the Application

python app.py

Open your browser and visit:

http://127.0.0.1:5000/

---

## 📥 Supported Inputs

### Facial Image
- Supported formats: .jpg, .png  
- Clear frontal face recommended  
- Good lighting improves accuracy  

### Voice Recording
- Supported formats: .wav, .mp3  
- Short and clear speech samples recommended  
- Low background noise preferred  

---

## 🧪 Testing Summary

- User authentication testing  
- Image upload and preprocessing validation  
- Voice upload and processing verification  
- AI model response validation  
- Chatbot domain restriction testing  
- Error and exception handling  

---

## 📊 Performance Overview

| Module | Average Time |
|------|-------------|
| Image Preprocessing | ~0.18 sec |
| Image AI Analysis | 1.2 – 2.5 sec |
| Audio AI Analysis | 1.4 – 2.2 sec |
| Chatbot Response | ~1.5 sec |

---

## ⚠️ Limitations

- Accuracy may reduce with poor lighting conditions  
- Noisy audio may affect speech analysis results  
- System is not clinically validated  
- AI output depends on prompt quality and input clarity  

---

## 🔮 Future Scope

- Integration of CNNs and Vision Transformers  
- Advanced speech signal processing techniques  
- Mobile application development  
- Real-time camera and microphone analysis  
- Clinical dataset validation  
- Explainable AI (XAI) integration  

---

## 📜 License

This project is developed for academic and educational purposes only. Medical or commercial deployment requires professional validation.
