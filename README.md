# ResumeMatcher

### AI-Powered Resume Screening & Ranking System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B)
![NLP](https://img.shields.io/badge/AI-HuggingFace-yellow)

**ResumeMatcher** is an intelligent recruitment tool designed to automate the initial screening process. Unlike traditional ATS (Applicant Tracking Systems) that rely on simple keyword matching, ResumeMatcher uses **Semantic NLP Models (SBERT)** to understand the context and meaning of candidate resumes, providing a relevance score based on the actual job description.

## Features

*   **Semantic Analysis**: Uses `all-MiniLM-L6-v2` transformers to understand context, not just keywords.
*   **Interactive Dashboard**: Visualizes match scores with high-contrast, professional charts.
*   **Multi-Format Support**: Handles bulk uploads of both PDF and DOCX files.
*   **Enterprise UI**: Features a "Corporate Midnight" dark mode for a premium user experience.
*   **Secure Processing**: All processing happens locally/in-memory; no data is stored permanently.

## Tech Stack

*   **Frontend**: Streamlit
*   **Logic**: Python 3.14+
*   **NLP Engine**: `sentence-transformers` (Hugging Face)
*   **Data Processing**: Pandas, PyPDF2, Python-Docx
*   **Visualization**: Plotly Express

## Quick Start

1.  **Clone the repository**
    ```bash
    git clone https://github.com/alcho-prof/Resume-Matcher.git
    cd Resume-Matcher
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application**
    ```bash
    streamlit run app.py
    ```

4.  **Open browser**: Go to `http://localhost:8501`

## Contributing

Contributions are welcome! This project is open-source and we'd love to see what you can add.
1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/NewFeature`).
3.  Commit your changes.
4.  Push to the branch.
5.  Open a Pull Request.

---
**Signature**: JD aka alcho-prof