# System Architecture: AI Smart Screening System

## 1. Executive Summary
The **AI Smart Screening System** ("ResumeMatcher") is a specialized Natural Language Processing (NLP) application designed to automate the initial screening phase of recruitment. It leverages transformer-based language models to semantically compare candidate resumes against job descriptions, providing a quantitative relevance score that goes beyond keyword matching.

## 2. Technical Stack

| Component | Technology | Role |
|-----------|------------|------|
| **Frontend** | Streamlit (Python) | Interactive UI, state management, and component rendering. |
| **Styling** | CSS3 (Custom Injection) | "Corporate Midnight" theme, responsive layout, custom card designs. |
| **NLP Engine** | `sentence-transformers` | Semantic embedding generation using Hugging Face models. |
| **Data Processing** | `pandas`, `PyPDF2`, `python-docx` | ETL (Extract, Transform, Load) pipeline for unstructured document data. |
| **Visualization** | Plotly Express | Interactive, high-contrast statistical charts. |
| **Runtime** | Python 3.14+ | Core execution environment. |

## 3. High-Level Architecture

The system follows a **Streamlit Monolithic Architecture** where the UI and Logic reside in the same execution loop, but are logically separated into presentation (`app.py`) and business logic (`utils.py`).

```mermaid
graph TD
    User[Recruiter] -->|Uploads PDF/DOCX| GUI[Streamlit UI]
    User -->|Inputs Job Description| GUI
    
    subgraph "Application Layer (app.py)"
        GUI -->|Triggers Analysis| Controller
        Controller -->|Visualizes| Dashboard[Plotly Charts & Ranking Cards]
    end
    
    subgraph "Logic Layer (utils.py)"
        Controller -->|Raw File| Extractor[Text Extractor]
        Extractor -->|Clean Text| Chunker[Semantic Chunker]
        
        Chunker -->|Text Chunks| Model[SBERT Model]
        Model -->|Embeddings| Matcher[Similarity Engine]
        
        Matcher -->|Relevance Score| Controller
    end
    
    subgraph "Infrastructure"
        Model -->|Loads| HF[Hugging Face Hub]
        style[style.css] -.->|Injects| GUI
    end
```

## 4. detailed Component Breakdown

### 4.1. The User Interface (`app.py`)
*   **Role**: Orchestrates the user flow and renders the application state.
*   **Key Features**:
    *   **State Management**: Handles file uploads and input persistence during re-runs.
    *   **Asset Injection**: Reads `style.css` and injects it via `st.markdown(unsafe_allow_html=True)` to override default Streamlit styles for a custom, premium look.
    *   **Defensive Design**: Validates inputs (file presence, JD length) before invoking expensive compute operations.

### 4.2. The Intelligence Engine (`utils.py`)
This module encapsulates the functional core of the application.

#### A. Ingestion & Extraction
*   **PDF Parsing**: Uses `PyPDF2` to iterate through pages and extract text strings.
*   **DOCX Parsing**: Uses `python-docx` to extract text from paragraph elements.
*   **Normalization**: Basic whitespace cleaning is performed to prepare text for the model.

#### B. Semantic Chunking
*   **Problem**: Transformer models have a maximum token context window (typically 512 tokens). Resumes often exceed this.
*   **Solution**: The `chunk_text` function implements a sliding window approach:
    *   **Window Size**: ~500 characters (configurable via UI).
    *   **Overlap**: ~50 characters (preserves context between chunks).
    *   **Benefit**: Ensures no critical information is lost at the boundaries of a chunk.

#### C. Vector Embedding & Matching
*   **Model**: `all-MiniLM-L6-v2`
    *   Selected for its optimal trade-off between speed (low latency on CPU) and accuracy.
    *   Maps sentences & paragraphs to a 384-dimensional dense vector space.
*   **Algorithm**:
    1.  **Encode**: Convert Job Description ($V_{jd}$) and Resume Chunks ($V_{r1}, V_{r2}...$) into vectors.
    2.  **Compare**: Calculate **Cosine Similarity** between $V_{jd}$ and every resume chunk vector.
    3.  **Aggregate**: The *score* for a candidate is defined as the **Maximum Similarity Score** found in any single chunk.
    $$ Score = \max( \cos(\theta) ) $$
    *   *Rationale*: A resume is relevant if *part* of it strongly matches the JD (e.g., a specific project or skills section), even if other parts ( education, hobbies) do not.

## 5. Deployment Considerations

*   **Concurrency**: Streamlit is single-threaded per session. For high usage, multiple workers or container orchestration (Docker/K8s) is recommended.
*   **Cold Start**: The model download occurs on the first run. In production, the model path should be cached or baked into a Docker image.
*   **Security**: File uploads are processed in-memory and not persisted to disk to ensure data privacy (GDPR considerations).

## 6. Future Roadmap

1.  **Queue System**: Offload processing to Celery/Redis for non-blocking UI.
2.  **LLM Integration**: Use Generative AI (Gemini/GPT) to provide *qualitative* feedback (e.g., "Why is this a good match?") alongside the score.
3.  **Database**: Persist candidate profiles in a vector database (e.g., ChromaDB, Pinecone) for historical search.
