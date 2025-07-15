# main.py
import docx
import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import (ChatGoogleGenerativeAI,
                                    GoogleGenerativeAIEmbeddings)
from PyPDF2 import PdfReader

from search_history import (display_user_history, initialize_database,
                            store_search_query)

initialize_database()

# ---------- Session Auth Check ----------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔐 Please login to access this page.")
    st.stop()

username = st.session_state.username
st.set_page_config(page_title="RAG Chatbot", layout="wide")
st.title(f"📄 RAG QA Bot — Welcome, {username}")

# ---------- File Readers ----------
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    return "".join([page.extract_text() or "" for page in reader.pages])

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_data_from_csv(file):
    try:
        df = pd.read_csv(file)
    except UnicodeDecodeError:
        file.seek(0)
        df = pd.read_csv(file, encoding="latin1")
    return df.to_csv(index=False)

def extract_text_from_txt(file):
    content = file.read()
    return content.decode("utf-8", errors="ignore") if isinstance(content, bytes) else content

def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        return "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
    except Exception as e:
        st.error(f"Failed to fetch or parse URL: {e}")
        return ""

# ---------- LangChain Functions ----------
api_key = "AIzaSyClWxop1Uag0XKwP1uH40AHttLX5QoAVJw"  # Replace with your actual key


def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=500)
    return splitter.split_text(text)

def get_vector_store(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    vector_store.save_local(f"faiss_index/faiss_index_{username}")

def get_conversational_chain():
    prompt_template = """
    Use the context below to answer the question accurately.
    If the answer is not found, say: "Answer is not available in the context."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    model = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", temperature=0.3, google_api_key=api_key)
    return load_qa_chain(model, chain_type="stuff", prompt=prompt)

def get_answer(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    vector_store = FAISS.load_local(f"faiss_index/faiss_index_{username}", embeddings, allow_dangerous_deserialization=True)
    docs = vector_store.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    return response["output_text"]

# ---------- Sidebar UI ----------
with st.sidebar:
    st.header("📂 Input Method")
    option = st.radio("Choose:", ["Upload Files", "Enter URL"])
    uploaded_files = None
    url_input = ""

    if option == "Upload Files":
        uploaded_files = st.file_uploader("Upload PDF, DOCX, CSV, TXT", accept_multiple_files=True)
    else:
        url_input = st.text_input("Enter URL")

    process = st.button("Submit & Process")

    if st.button("Logout"):
        st.session_state.clear()
        st.success("You have been logged out.")
        st.switch_page("login.py")

# ---------- Main Logic ----------
if process:
    full_text = ""

    if option == "Upload Files" and uploaded_files:
        for file in uploaded_files:
            if file.name.endswith(".pdf"):
                full_text += extract_text_from_pdf(file)
            elif file.name.endswith(".docx"):
                full_text += extract_text_from_docx(file)
            elif file.name.endswith(".csv"):
                full_text += extract_data_from_csv(file)
            elif file.name.endswith(".txt"):
                full_text += extract_text_from_txt(file)
            else:
                st.warning(f"{file.name} is not supported.")
    elif option == "Enter URL" and url_input.strip():
        full_text += extract_text_from_url(url_input.strip())
    else:
        st.warning("Please upload a file or enter a valid URL.")

    if full_text.strip():
        st.session_state["ready"] = True
        chunks = get_text_chunks(full_text)
        get_vector_store(chunks)
        st.success("✅ Content processed successfully! You can now ask questions.")

# ---------- Q&A Section ----------
if st.session_state.get("ready"):
    st.markdown("### ❓ Ask a Question")
    user_question = st.text_input("Your question:")
    if user_question:
        with st.spinner("Thinking..."):
            answer = get_answer(user_question)
            store_search_query(username, user_question, answer)


            st.markdown(f"**🤖 Answer:** {answer}")
            display_user_history()

