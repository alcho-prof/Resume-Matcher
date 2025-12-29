import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_model, extract_text, chunk_text, calculate_similarity

# --- Page Configuration ---
st.set_page_config(
    page_title="Resume Matching System",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Load Custom CSS ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# --- Initialize Model ---
# Show a simple text spinner
with st.spinner("System Initializing..."):
    model = load_model()

# --- Application Layout ---

# Sidebar for Inputs
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/resume.png", width=100)
    st.title("ResumeMatcher")
    
    st.subheader("Document Upload")
    uploaded_files = st.file_uploader(
        "Upload PDF or DOCX files", 
        type=['pdf', 'docx'], 
        accept_multiple_files=True
    )
    
    st.markdown("---")
    st.subheader("Settings")
    chunk_size = st.slider("Chunk Size", 200, 1000, 500, help="Character count per text chunk for analysis")
    
    st.markdown("---")
    st.caption("Signature: JD aka alcho-prof")

# Main Content Area
col_header, col_logo = st.columns([4, 1])
with col_header:
    st.markdown("""
    # AI Smart Screening
    ### Intelligent Resume Ranking System
    """)
    st.markdown("Optimize your recruitment process with semantic matching.")


# Job Description Input
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Job Description")
    job_description = st.text_area(
        "Enter the job requirements below:",
        height=250,
        placeholder="Past the full job description here..."
    )

with col2:
    st.subheader("Process Details")
    st.markdown("""
    **Algorithm:** Hugging Face Transformer (all-MiniLM-L6-v2)
    
    **Workflow:**
    1. Text Extraction
    2. Semantic Chunking
    3. Vector Embedding
    4. Similarity Calculation
    """)
    analyze_button = st.button("Calculate Matches")

# --- Logical Flow ---

if analyze_button:
    if not job_description:
        st.error("Error: Job Description is required.")
    elif not uploaded_files:
        st.error("Error: No resume files uploaded.")
    else:
        results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, file in enumerate(uploaded_files):
            status_text.text(f"Processing file: {file.name}")
            
            # 1. Text Extraction
            text = extract_text(file)
            
            # 2. Chunking
            chunks = chunk_text(text, chunk_size=chunk_size)
            
            # 3. AI Matching
            score = calculate_similarity(model, job_description, chunks)
            
            results.append({
                "Filename": file.name,
                "Score": score,
                "Match Percentage": f"{round(score * 100, 2)}%",
                "Text Preview": text[:200] + "..." if text else "No text found"
            })
            
            # Update Progress
            progress_bar.progress((i + 1) / len(uploaded_files))
        
        status_text.empty()
        progress_bar.empty()
        
        
        # --- Visualization & Report ---
        st.divider()
        st.subheader("Analysis Report")
        
        # Sort results
        df = pd.DataFrame(results).sort_values(by="Score", ascending=False)
        
        # Layout: Chart on Left, Top Matches on Right
        viz_col, list_col = st.columns([1.5, 1])
        
        with viz_col:
            st.markdown("### Match Overview")
            if not df.empty:
                fig = px.bar(
                    df, 
                    x="Score", 
                    y="Filename", 
                    orientation='h',
                    text="Match Percentage",
                    color="Score",
                    color_continuous_scale=['#1e293b', '#3b82f6', '#10b981'] # Gradient from dark to accent
                )
                fig.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)", # Transparent
                    paper_bgcolor="rgba(0,0,0,0)", # Transparent
                    font_color="#94a3b8",
                    xaxis_title="Relevance Score",
                    yaxis_title=None,
                    height=400,
                    margin=dict(l=0, r=0, t=0, b=0),
                    yaxis={'categoryorder':'total ascending'},
                    coloraxis_showscale=False
                )
                fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#334155')
                fig.update_traces(textposition='inside', textfont=dict(color='white'))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data to visualize.")

        with list_col:
            st.markdown("### Top Candidates")
            if not df.empty:
                for index, row in df.iterrows():
                    # Custom HTML Card for each result
                    st.markdown(f"""
                    <div class="result-card">
                        <div>
                            <div class="file-name">{row['Filename']}</div>
                            <div style="font-size: 0.8rem; color: #94a3b8;">
                                {row['Text Preview'][:80]}...
                            </div>
                        </div>
                        <div class="score-badge">{row['Match Percentage']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.write("No files processed.")

        # Detailed Data Table (Hidden by default or smaller)
        with st.expander("📄 View Raw Data"):
            st.dataframe(
                df[["Filename", "Match Percentage", "Score"]],
                use_container_width=True,
                hide_index=True
            )
            


# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 0.8rem;'>"
    "Resume Classification System | HR Technology Division</div>", 
    unsafe_allow_html=True
)
