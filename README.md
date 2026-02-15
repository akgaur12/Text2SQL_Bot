# 🤖 SQLify | Text-to-SQL Bot

SQLify is an intelligent platform designed to bridge the gap between users and data. It leverages advanced Large Language Models (LLMs) via **LlamaIndex** to convert natural language queries into executable **SQLite** commands, providing instantaneous insights from structured data.

---

## ✨ Key Features

- **Natural Language Processing**: Simply ask questions like "Who are the highest-paid employees?" and get immediate SQL results.
- **Modern & Responsive UI**: A sleek, mobile-first interface designed with vanilla CSS for maximum speed and flexibility.
- **Intelligent Table Handling**: Complex SQL results are rendered in beautifully styled, horizontally scrollable tables.
- **Production-Ready Core**: Standardized logging, robust error handling, and secure SQL validation.

---

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **AI/LLM**: LlamaIndex, Groq / Ollama (via LlamaIndex-LLMS)
- **Database**: SQLite3
- **Frontend**: HTML5, Vanilla CSS, Modern JavaScript (Fetch API)
- **Styling**: Google Fonts (Inter), FontAwesome icons

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- (Optional) [Ollama](https://ollama.com/) for local LLM support.
- Groq API Key (if using Groq).

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/akgaur12/Text2SQL_Bot.git
   cd Text2SQL_Bot
   ```

2. **Set up a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the application**:
   - Create a `.env` file and add your credentials (e.g., `GROQ_API_KEY`).
   - Modify `config/config.yml` to switch between models or adjust server settings.

---

## 🏃 Running the App

Start the development server:

```bash
python3 app.py

or

gunicorn -c gunicorn_config.py app:app
```

Open your browser and navigate to `http://127.0.0.1:5001`.

---

## 📂 Project Structure

```text
├── config/              # YAML configuration files
├── resources/           # Database files (.db)
├── src/                 # Core logic (LlamaIndex pipeline, utilities)
├── static/              # CSS, JS, and image assets
├── templates/           # HTML templates (Flask/Jinja2)
├── app.py               # Application entry point
└── requirements.txt     # Python dependencies
```

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---