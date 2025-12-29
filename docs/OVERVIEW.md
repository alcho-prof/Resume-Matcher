# Resume Classification and Matching System - Project Documentation

## 1. Project Overview & Workflow

### **What is this?**
This is an AI-powered HR tool designed to streamline the recruitment process. It allows HR professionals to upload multiple resumes (PDF or DOCX) and a Job Description (JD). The system then uses a **Pretrained Hugging Face Transformer Model** to "read" the resumes and the JD, understand their semantic meaning, and output a compatibility score for each resume.

### **How it Works (The Workflow)**
1.  **Input**: The user provides a Job Description (Text) and uploads Resume documents (Files).
2.  **Text Extraction**: The app reads the raw files and converts them into string text.
3.  **Chunking**: Large text (like a full resume) is split into smaller pieces ("chunks") because AI models have a limit on how much text they can process at once.
4.  **Embedding (The AI Magic)**: The text chunks and the JD are sent to the **Hugging Face Model**. The model converts this text into numeric lists called "Vectors" or "Embeddings".
    *   *Think of this as translating English into a "language of numbers" that represents meaning.*
5.  **Similarity Calculation**: The system compares the numbers of the JD vs. the Resume using **Cosine Similarity**. If the numbers point in the same direction, the meaning is similar.
6.  **Ranking**: Resumes are ranked by their similarity scores and displayed.

---

## 2. Libraries & Dependencies

These are the tools we installed in `requirements.txt`.

| Library | Purpose in this Project |
| :--- | :--- |
| **`streamlit`** | The web framework used to build the user interface (buttons, file uploaders, layout) without knowing HTML/JS. |
| **`sentence-transformers`** | A Hugging Face library. It provides the easy interface to download and use the specific AI model (`all-MiniLM-L6-v2`) for creating sentence embeddings. |
| **`torch`** | PyTorch. This is the deep learning engine that powers the Transformer model. It handles the heavy matrix math. |
| **`PyPDF2`** | A utility to open and read text from PDF files. |
| **`python-docx`** | A utility to open and read text from Microsoft Word (.docx) files. |
| **`plotly`** | Used to create the interactive, beautiful bar charts for the results. |
| **`pandas`** | Used to organize the results (filenames, scores) into a structured table (DataFrame) for easy sorting and graphing. |

---

## 3. Deep Dive: `utils.py`

This file contains the "brain" or the backend logic of the application. It handles data processing and AI.

### **Initial Imports**
```python
import streamlit as st
from sentence_transformers import SentenceTransformer, util
import PyPDF2
from docx import Document
import torch
```
*   We import `sentence_transformers` to access the model.
*   `util` from `sentence_transformers` gives us the "cosine similarity" math function.

### **Function 1: `load_model()`**
```python
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')
```
*   **`@st.cache_resource`**: This is a Streamlit decorator. Loading an AI model takes time (seconds) and memory. This line tells the app: *"Run this function ONLY ONCE. If the user clicks a button, don't reload the model, just use the one already in memory."*
*   **`SentenceTransformer('all-MiniLM-L6-v2')`**: This downloads the specific model from Hugging Face.
    *   **Why `all-MiniLM-L6-v2`?**: It is an incredibly fast and lightweight model (approx 80MB) that performs very well on semantic search tasks. It balances speed and accuracy perfectly for a resume matcher.

### **Function 2: `extract_text_from_pdf(uploaded_file)`**
```python
def extract_text_from_pdf(uploaded_file):
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e: ...
```
*   **Why**: Computers can't read PDF files directly like text files. We need a parser.
*   **Logic**: We create a `PdfReader`, loop through every page, extract the text, and join it into one long string.

### **Function 3: `extract_text_from_docx(uploaded_file)`**
```python
def extract_text_from_docx(uploaded_file):
    try:
        doc = Document(uploaded_file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e: ...
```
*   **Why**: Similar to PDF, Word docs are complex XML zip files. `python-docx` helps us read them.
*   **Logic**: We loop through every "paragraph" in the document and combine the text.

### **Function 4: `chunk_text(text, chunk_size=500, overlap=50)`**
```python
def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])
    return chunks
```
*   **Why (Critical)**: Transformer models usually have a limit (e.g., 512 tokens). If a resume is 2 pages long, the model cuts off the end.
*   **Logic**: We cut the text into smaller pieces (chunks) so we can analyze each piece separately to find the best matching section.
*   `overlap=50`: We overlap slightly so we don't accidentally cut a keyword in half (e.g., cutting "Engin" and "eer" separately).

### **Function 5: `calculate_similarity(model, job_description, chunks)`**
```python
def calculate_similarity(model, job_description, chunks):
    # 1. Convert text to numbers (Embeddings)
    jd_embedding = model.encode(job_description, convert_to_tensor=True)
    chunk_embeddings = model.encode(chunks, convert_to_tensor=True)
    
    # 2. Math comparison (Cosine Similarity)
    cosine_scores = util.cos_sim(jd_embedding, chunk_embeddings)
    
    # 3. Get the max score
    return torch.max(cosine_scores).item()
```
*   **`model.encode`**: This is the heavy lifting. It converts the JD string and the list of resume chunks into tensors (matrices of numbers).
*   **`util.cos_sim`**: Performs cosine similarity. Result 1.0 = Exact match. Result 0.0 = No relation.
*   **`torch.max`**: Since we split the resume into chunks, we might get 5 scores for one resume. We take the **highest** score because that represents the part of the resume that best matches the job text.

---

## 4. Deep Dive: `app.py`

This file is the Frontend. It controls what the user sees.

### **Setup & Styling**
```python
st.set_page_config(...)
def local_css(file_name): ...
```
*   Sets the browser tab title and favicon.
*   Injects the CSS from `style.css` into the page to apply the custom "Glassmorphism" look.

### **Main Logic Flow**

1.  **Sidebar**:
    ```python
    uploaded_files = st.file_uploader(..., accept_multiple_files=True)
    ```
    *   Creates the drag-and-drop box. `accept_multiple_files=True` is crucial for bulk processing.

2.  **Job Description Input**:
    ```python
    job_description = st.text_area(...)
    ```
    *   A large text box for pasting the requirement.

3.  **The "Analyze" Loop**:
    ```python
    if analyze_button:
        for i, file in enumerate(uploaded_files):
            # Calls the functions we defined in utils.py
            text = extract_text(file)
            chunks = chunk_text(text, chunk_size=chunk_size)
            score = calculate_similarity(model, job_description, chunks)
            ...
    ```
    *   This is the core loop. It iterates through every file uploaded, processes it using our utility functions, and saves the score.

4.  **Displaying Results**:
    ```python
    df = pd.DataFrame(results).sort_values(by="Score", ascending=False)
    fig = px.bar(...)
    st.plotly_chart(fig)
    ```
    *   We convert the list of results into a `pandas` DataFrame. This makes sorting by score ("Best to Worst") one line of code.
    *   `px.bar`: Creates the horizontal bar chart.

---

## 5. Deep Dive: `style.css`

This file is purely for aesthetics ("The Wow Factor").

*   `background: linear-gradient(...)`: Gives the deep blue/purple modern background.
*   `.stApp`: Targets the main container.
*   `backdrop-filter: blur(10px)`: This creates the "frosted glass" effect on the cards.
*   `h1`: Gradients on text (green to blue).

---
