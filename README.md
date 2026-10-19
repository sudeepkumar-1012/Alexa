# Alexa


# 🔵 Alexa AI Assistant

A Python-based AI voice assistant built using Flask and Google's Gemini API. It provides an interactive web interface where users can ask questions, use voice input, and listen to AI-generated responses.

## ✨ Features

- 🤖 **AI-powered conversations** using the Gemini API
- 🎙️ **Voice input** using browser speech recognition
- 🔊 **Text-to-speech** for spoken AI responses
- 💬 **Interactive chat interface** with message history
- 🕒 **Date and time responses**
- 📱 **Responsive UI** built with HTML and CSS
- 🔐 **Environment-based API key configuration**

## 🛠️ Technologies Used

- Python
- Flask
- Google Gemini API
- HTML5
- CSS3
- JavaScript
- Speech Recognition API
- Web Speech Synthesis API
- python-dotenv

## 📂 Project Structure

```text
Alexa-AI/
├── Alexa_AI.py
├── .env
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd YOUR_REPOSITORY_FOLDER
```

Replace the placeholders with your actual GitHub repository URL and folder name.

### 2. Install dependencies

```bash
python -m pip install flask google-genai python-dotenv
```

### 3. Configure the API key

Create a `.env` file in the project directory:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Get your API key from [Google AI Studio](https://aistudio.google.com/apikey).

**Security:** Never commit your `.env` file or publish your API key.

### 4. Run the application

```bash
python Alexa_AI.py
```

### 5. Open in your browser

Visit:

```text
http://127.0.0.1:5001
```

## 🎙️ How to Use

1. Start the Flask application.
2. Open the application in your browser.
3. Type a question or click the **Speak** button.
4. Receive an AI-generated response.
5. Listen to the response using text-to-speech.

Voice input requires browser support, microphone permission, and a working speech-recognition service.

## 🔑 Environment Variables

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | API key used to access Google's Gemini API |

## 🚀 Future Enhancements

- Wake-word detection for hands-free activation
- Improved microphone and speech recognition support
- Weather information and website-opening commands
- Conversation memory
- Additional voice and language options

## 👨‍💻 Author

**Sudeep Kumar R V**

Aspiring Python Full Stack Developer

## 📄 License

This project is available for educational and personal learning purposes. Add an appropriate open-source license if you intend to distribute it under specific reuse terms.