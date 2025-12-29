import streamlit as st
from sentence_transformers import SentenceTransformer, util
import PyPDF2
from docx import Document
import torch

@st.cache_resource
def load_model():
    """Loads the pretrained Sentence Transformer model."""
    # Using a lightweight but effective model for semantic search
    return SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_pdf(uploaded_file):
    """Extracts text from a PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_docx(uploaded_file):
    """Extracts text from a DOCX file."""
    try:
        doc = Document(uploaded_file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

def extract_text(uploaded_file):
    """Router to extract text based on file type."""
    if uploaded_file.name.endswith('.pdf'):
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith('.docx'):
        return extract_text_from_docx(uploaded_file)
    else:
        return "Unsupported file format."

def chunk_text(text, chunk_size=500, overlap=50):
    """
    Splits text into chunks of approximately 'chunk_size' characters 
    to handle long resumes and stay within model token limits.
    """
    if not text:
        return []
    
    chunks = []
    # accurate splitting should be done by tokens, but char count is a fast heuristic
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])
    return chunks

def calculate_similarity(model, job_description, chunks):
    """
    Computes similarity scores for chunks against the job description.
    Returns the maximum similarity score found in the chunks.
    """
    if not chunks:
        return 0.0
        
    # Encode JD and Chunks
    jd_embedding = model.encode(job_description, convert_to_tensor=True)
    chunk_embeddings = model.encode(chunks, convert_to_tensor=True)
    
    # Compute Cosine Similarity
    cosine_scores = util.cos_sim(jd_embedding, chunk_embeddings)
    
    # Return the highest score among all chunks (best match section)
    # Item() converts a single value tensor to a standard Python number
    return torch.max(cosine_scores).item()
