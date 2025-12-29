# Zero-Cost Deployment Guide

Targeting **Streamlit Community Cloud** is the best option for free, persistent hosting of this application. It connects directly to your GitHub repository.

## Option 1: Streamlit Community Cloud (Recommended)

### Prerequisites
1.  A [GitHub Account](https://github.com/).
2.  A [Streamlit Cloud Account](https://streamlit.io/cloud) (you can sign up with GitHub).

### Step 1: Prepare Repository
The project must be stored on GitHub.
1.  Initialize Git (if not already done):
    ```bash
    git init
    git add .
    git commit -m "Initial commit of Resume Matcher"
    ```
2.  Create a **New Repository** on GitHub.
3.  Push your code:
    ```bash
    git remote add origin https://github.com/YOUR_USERNAME/resume-matcher.git
    git branch -M main
    git push -u origin main
    ```

### Step 2: Deploy
1.  Go to **[share.streamlit.io](https://share.streamlit.io/)**.
2.  Click **"New app"**.
3.  Select your repository (`resume-matcher`).
4.  Select the branch (`main`).
5.  Set "Main file path" to `app.py`.
6.  Click **"Deploy!"**.

### Step 3: Post-Deployment Configuration
*   **Model Caching**: The first time the app runs, it will download the model (`all-MiniLM-L6-v2`). This might take a minute. Streamlit Cloud caches this, so subsequent runs are fast.
*   **Secrets**: If you add any API keys later, use the "Secrets" settings in the dashboard.

---

## Option 2: Hugging Face Spaces

This is also an excellent free option, especially since we use Hugging Face models.

1.  Create a **[Hugging Face Account](https://huggingface.co/join)**.
2.  Go to **[Spaces](https://huggingface.co/spaces)** and click **"Create new Space"**.
3.  **Name**: `resume-matcher`
4.  **SDK**: Choose `Streamlit`.
5.  **Hardware**: Choose `CPU basic` (Free).
6.  **Files**: Upload your files (`app.py`, `utils.py`, `style.css`, `requirements.txt`) directly via the web interface OR clone the repo they give you and push your code there.
    ```bash
    git clone https://huggingface.co/spaces/YOUR_USERNAME/resume-matcher
    cp -r /path/to/your/project/* .
    git add .
    git commit -m "Deploy app"
    git push
    ```

## Critical Verification
Ensure your `requirements.txt` is present in the root directory. The cloud build server needs this to install `sentence-transformers`, `streamlit`, and other libraries.
