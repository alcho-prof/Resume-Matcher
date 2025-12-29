# Function Analysis: `extract_text and DOCX`

## 1. The Full Code
```python
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
```

## 2. What do these functions do?
1.  **`extract_text_from_docx`**: Specifically handles Microsoft Word files.
2.  **`extract_text`**: The "Traffic Controller" (Router). It looks at the file extension and decides which specialist function (PDF vs DOCX) should handle the job.

---

## 3. Top-to-Bottom Line Explanation (DOCX)

### Line: `doc = Document(uploaded_file)`
*   **The Constructor**: `Document(...)` from the `python-docx` library.
*   **What it does**: A `.docx` file is actually a zipped folder of XML files. This constructor unzips it in memory and organizes it into valid paragraphs, tables, and styles so Python can traverse it.

### Line: `for para in doc.paragraphs:`
*   **What is it?**: A Loop.
*   **Why**: Word documents are made of "Paragraphs". Even a blank line is a paragraph. We loop through every single paragraph block in the document.

### Line: `text += para.text + "\n"`
*   **`para.text`**: This extracts *only* the visible words from that paragraph block (ignoring bold/italic styling codes).

---

## 4. Top-to-Bottom Line Explanation (Router)

### Line: `if uploaded_file.name.endswith('.pdf'):`
*   **Logic**: Checks the actual filename (e.g., "Resume.pdf").
*   **Action**: If it ends in `.pdf`, it calls the `extract_text_from_pdf` function.

### Line: `elif uploaded_file.name.endswith('.docx'):`
*   **Logic**: Else-If. If it wasn't a PDF, is it a Word doc?
*   **Action**: Calls `extract_text_from_docx`.

### Line: `else:`
*   **Fallback**: If the user uploaded a `.jpg` or `.txt`, we don't know how to handle it. We returns an error string.
