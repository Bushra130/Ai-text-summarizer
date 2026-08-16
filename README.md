# 📝 AI Text Summarization Tool

An AI-powered text summarization tool built with Python, Streamlit, and a pre-trained NLP model.

## 📌 About the Project

This application uses Artificial Intelligence to generate concise summaries from text and uploaded documents.

Users can enter text directly or upload PDF, DOCX, and TXT files. The application extracts the text and generates a summary based on the selected summary length.

## ✨ Features

* 📝 Summarize manually entered text
* 📄 Upload and summarize PDF files
* 📘 Upload and summarize DOCX files
* 📃 Upload and summarize TXT files
* 🤖 AI-powered summarization using BART
* 📏 Choose Short, Medium, or Long summaries
* 📊 View original and summary word counts
* 📉 Calculate percentage of text reduction
* 🧠 Extract key topics from the input text
* 📋 Copy the generated summary

## 🛠️ Technologies Used

* Python
* Streamlit
* Hugging Face Transformers
* BART (`facebook/bart-large-cnn`)
* PyPDF
* python-docx
* YAKE

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Bushra130/AI-text-summarizer.git
cd AI-text-summarizer
```

### 2. Install the required libraries

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
streamlit run app.py
```

The application will open in your web browser.

## 📂 Project Structure

```text
AI-text-summarizer/
├── app.py
├── requirements.txt
└── README.md
```

## 🤖 AI Model

The application uses the pre-trained **BART Large CNN** model from Hugging Face for abstractive text summarization.

## 👩‍💻 Author

**Bushra130**

## 📚 Acknowledgements

* Hugging Face Transformers
* Streamlit
* PyPDF
* python-docx
* YAKE
