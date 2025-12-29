# Function Analysis: `chunk_text`

## 1. The Full Code
```python
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
```

## 2. What does this function do?
Imagine trying to eat a whole large pizza in one bite. You can't. You need to slice it.
AI Models work the same way. They have a "Context Window" (usually 512 words). If a resume has 2000 words, the AI will crash or ignore the last 1500 words.
**Chunking** slices the long text into smaller, bite-sized pieces so the AI can process piece-by-piece.

---

## 3. Top-to-Bottom Line Explanation

### Line: `def chunk_text(text, chunk_size=500, overlap=50):`
*   **Arguments**:
    *   `text`: The huge string of text (e.g., entire resume).
    *   `chunk_size=500`: Default slice size is 500 characters.
    *   `overlap=50`: **Crucial Concept**. We don't slice cleanly (0-500, 500-1000). We slice with overlap (0-500, 450-950).
    *   **Why Overlap?**: Context. Imagine the sentence was "I am an expert in Python." If we slice right between "expert" and "in", Chunk A sees "I am an expert", Chunk B sees "in Python." Neither chunk sees the full thought. Overlapping ensures no key phrase is cut in half.

### Line: `if not text: return []`
*   **Safety**: If the resume was blank, return an empty list.

### Line: `for i in range(0, len(text), chunk_size - overlap):`
*   **The Loop Logic**:
    *   Start at 0.
    *   Go until the end of the text (`len(text)`).
    *   **Step Size**: `chunk_size - overlap` (e.g., 500 - 50 = 450).
    *   So `i` will be: 0, 450, 900, 1350...

### Line: `chunks.append(text[i:i + chunk_size])`
*   **Slicing**: Python Slicing `[start:end]`.
*   We take the text starting at `i` and ending at `i + 500`.
*   We throw this slice into our `chunks` list.
*   **Result**: A list of strings, each 500 chars long.
