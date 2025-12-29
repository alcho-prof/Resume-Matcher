# Function Analysis: `extract_text_from_pdf`

## 1. The Full Code
```python
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
```

## 2. What does this function do?
Computers cannot simply "read" a PDF files they are images or complex formatted documents. This function acts as a translator, opening the PDF file, going page-by-page, and scraping the raw words off the page into a simple string of text that Python can understand.

---

## 3. Top-to-Bottom Line Explanation

### Line 1: `def extract_text_from_pdf(uploaded_file):`
*   **Input**: `uploaded_file` is the file object the user dropped into the website.

### Line 3: `try:`
*   **What is it?**: Error handling block.
*   **Why**: PDFs can be corrupted, password-protected, or weirdly formatted. We "try" to read it, but if something crashes, we don't want the whole website to break (see `except` block).

### Line 4: `pdf_reader = PyPDF2.PdfReader(uploaded_file)`
*   **The Constructor**: `PyPDF2.PdfReader(...)`
*   **Explanation**:
    *   `PyPDF2` is the library toolbelt.
    *   `PdfReader` is the specific tool.
    *   It takes the raw binary file (`uploaded_file`) and parses the internal structure of the PDF (headers, fonts, page layout). It creates a "Reader Object" that understands the file structure.

### Line 5: `text = ""`
*   **What is it?**: Variable Initialization.
*   **Why**: We start with an empty bucket (an empty string). We will throw text into this bucket as we find it on each page.

### Line 6: `for page in pdf_reader.pages:`
*   **What is it?**: A Loop (Iterator).
*   **English**: "For every single page that exists inside the PDF Reader object..."

### Line 7: `text += page.extract_text() + "\n"`
*   **`page`**: Represents the current page we are looking at.
*   **`extract_text()`**: A built-in method of the library that looks for letters/words on that specific page and returns them.
*   **`\n`**: This is a "Newline Character". It's like checking the "Enter" key.
*   **`+=`**: Append. We take the new text we found and glue it to the end of our existing `text` bucket.

### Line 8: `return text`
*   **Result**: Returns the final clean string containing all the words from the resume.

### Line 9-10: `except Exception as e:`
*   **Safety Net**: If anything failed above (e.g., file was encrypted), the code jumps here. It catches the specific error (`e`) and returns a helpful message instead of crashing.
