
# 🤖 RAG Chatbot with Login (Streamlit + Gemini)

A smart chatbot that answers questions from your uploaded files or website content using Google Gemini and LangChain.

---

## 🖼️ UI Preview

<img width="1914" height="814" alt="image" src="https://github.com/user-attachments/assets/58aa4c1f-1fb9-4a4c-8cb3-8de9b2a564de" />


---

## 🚀 Features

- 🔐 **User Login System** — Each user gets their own data access and session.
- 📄 **Upload Files** — Supports PDF, DOCX, CSV, and TXT formats.
- 🌐 **Enter URL** — Extract and process content from websites (e.g., https://docs.n8n.io).
- 🧠 **RAG Pipeline** — Combines LangChain + FAISS + Gemini for intelligent responses.
- 💬 **Interactive Q&A** — Ask questions directly from your data sources.
- 🌈 **Clean UI** — Built with Streamlit, modern dark-themed interface.
- 📝 **Chat History** — Review and reference previous queries and responses.

---

## 📦 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/rag-chatbot.git
cd rag-chatbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add Gemini API Key

Open `main.py` or `config.py` and replace the placeholder with your key:

```python
api_key = "your-gemini-api-key"
```

Or use a `.env` file with `python-dotenv` to keep it secure.

### 4. Run the App

```bash
streamlit run login.py
```

---

## ✅ Sample Use

**Q:** What is n8n?  
**A:** n8n is a fair-code-licensed workflow automation tool that combines AI capabilities with business process automation. It allows you to connect any app with an API to any other and manipulate its data with little or no code.

---

## 🧠 Tech Stack

- **Streamlit** – Frontend Interface
- **LangChain** – Retrieval Augmented Generation Logic
- **FAISS** – Vector Database for document similarity search
- **Google Gemini API** – Answer generation and reasoning
- **Python** – Backend scripting

---

## 📁 Folder Structure

```
rag-chatbot/
├── assets/
│   └── ui_screenshot.png       # ← Add your UI screenshot here
├── login.py
├── main.py
├── config.py
├── requirements.txt
└── README.md                   # ← This file
```
