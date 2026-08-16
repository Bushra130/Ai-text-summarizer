import streamlit as st
import streamlit.components.v1 as components
from transformers import pipeline
from pypdf import PdfReader
from docx import Document
import yake

st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="📝",
    layout="centered"
)

st.title("📝 AI Text Summarization Tool")
st.write("Summarize text and documents using Artificial Intelligence.")


@st.cache_resource
def load_model():
    return pipeline(
        "summarization",
        model="facebook/bart-large-cnn"
    )


summarizer = load_model()

# Choose input method
input_method = st.radio(
    "Choose input method:",
    ["📝 Enter Text", "📄 Upload PDF", "📘 Upload DOCX", "📃 Upload TXT"],
    horizontal=True
)

text = ""

# ---------------- TEXT INPUT ----------------

if input_method == "📝 Enter Text":

    text = st.text_area(
        "Enter your text:",
        height=250,
        placeholder="Paste your article or text here..."
    )


# ---------------- PDF INPUT ----------------

elif input_method == "📄 Upload PDF":

    uploaded_file = st.file_uploader(
        "Upload a PDF file:",
        type=["pdf"]
    )

    if uploaded_file is not None:

        try:
            reader = PdfReader(uploaded_file)

            for page in reader.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

            if text.strip():

                st.success(
                    f"✅ PDF loaded successfully! "
                    f"({len(reader.pages)} pages)"
                )

                st.text_area(
                    "Extracted Text:",
                    value=text,
                    height=200,
                    disabled=True
                )

            else:

                st.warning(
                    "⚠️ No readable text was found in this PDF."
                )

        except Exception:

            st.error("❌ Could not read this PDF.")


# ---------------- DOCX INPUT ----------------

elif input_method == "📘 Upload DOCX":

    uploaded_file = st.file_uploader(
        "Upload a DOCX file:",
        type=["docx"]
    )

    if uploaded_file is not None:

        try:

            document = Document(uploaded_file)

            paragraphs = []

            for paragraph in document.paragraphs:

                if paragraph.text.strip():
                    paragraphs.append(paragraph.text)

            text = "\n".join(paragraphs)

            if text.strip():

                st.success("✅ DOCX loaded successfully!")

                st.text_area(
                    "Extracted Text:",
                    value=text,
                    height=200,
                    disabled=True
                )

            else:

                st.warning(
                    "⚠️ No readable text was found in this DOCX."
                )

        except Exception:

            st.error("❌ Could not read this DOCX.")


# ---------------- TXT INPUT ----------------

elif input_method == "📃 Upload TXT":

    uploaded_file = st.file_uploader(
        "Upload a TXT file:",
        type=["txt"]
    )

    if uploaded_file is not None:

        try:

            text = uploaded_file.read().decode("utf-8")

            if text.strip():

                st.success("✅ TXT file loaded successfully!")

                st.text_area(
                    "File Content:",
                    value=text,
                    height=200,
                    disabled=True
                )

            else:

                st.warning(
                    "⚠️ The TXT file is empty."
                )

        except Exception:

            st.error("❌ Could not read this TXT file.")


# ---------------- SUMMARY LENGTH ----------------

summary_length = st.selectbox(
    "Choose summary length:",
    ["Short", "Medium", "Long"]
)

if summary_length == "Short":

    min_len = 30
    max_len = 60

elif summary_length == "Medium":

    min_len = 70
    max_len = 110

else:

    min_len = 120
    max_len = 160


# ---------------- SUMMARIZE ----------------

if st.button("✨ Summarize"):

    if not text.strip():

        st.warning(
            "⚠️ Please enter text or upload a document first."
        )

    elif len(text.split()) < 30:

        st.warning(
            "⚠️ Please provide at least 30 words "
            "for better summarization."
        )

    else:

        with st.spinner("🤖 Generating your summary..."):

            summary = summarizer(
                text,
                max_length=max_len,
                min_length=min_len,
                do_sample=False
            )[0]["summary_text"]

        original_words = len(text.split())

        summary_words = len(summary.split())

        reduction = (
            (original_words - summary_words)
            / original_words
        ) * 100

        st.subheader("📌 Summary")

        st.text_area(
            "Generated Summary",
            value=summary,
            height=180,
            disabled=True
        )

        # Copy button
        components.html(
            f"""
            <button onclick="copySummary()"
                style="
                    padding: 10px 20px;
                    font-size: 16px;
                    border-radius: 8px;
                    border: 1px solid #555;
                    background-color: #262730;
                    color: white;
                    cursor: pointer;
                ">
                📋 Copy Summary
            </button>

            <script>
            function copySummary() {{
                const text = {summary!r};

                navigator.clipboard.writeText(text).then(function() {{
                    alert("Summary copied to clipboard!");
                }});
            }}
            </script>
            """,
            height=55
        )

        # Statistics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Original Words", original_words)

        with col2:
            st.metric("Summary Words", summary_words)

        with col3:
            st.metric("Reduction", f"{reduction:.1f}%")

        # Keyword extraction
        kw_extractor = yake.KeywordExtractor(
            lan="en",
            n=2,
            dedupLim=0.95,
            top=8
        )

        keywords = kw_extractor.extract_keywords(text)

        st.subheader("🧠 Key Topics")

        keyword_text = " • ".join(
            [keyword for keyword, score in keywords]
        )

        st.info(keyword_text)
        
        st.success("✅ Summary generated successfully!")


st.divider()

st.caption(
    "Powered by AI • BART (facebook/bart-large-cnn) • Built with Streamlit"
)