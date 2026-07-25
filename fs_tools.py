import os
import datetime
import PyPDF2
import docx

def read_file(filepath: str) -> dict:
    """
    Read resume files (.pdf, .txt, .docx) and return content + metadata.
    """
    try:
        if filepath.endswith(".txt"):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        elif filepath.endswith(".pdf"):
            content = ""
            with open(filepath, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    content += page.extract_text() or ""
        elif filepath.endswith(".docx"):
            doc = docx.Document(filepath)
            content = "\n".join([para.text for para in doc.paragraphs])
        else:
            return {"status": "error", "message": "Unsupported file format"}

        metadata = {
            "filename": os.path.basename(filepath),
            "size": os.path.getsize(filepath),
            "modified_date": datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
        }
        return {"status": "success", "content": content, "metadata": metadata}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def list_files(directory: str, extension: str = None) -> list:
    """
    List all files in a directory, optionally filter by extension.
    """
    try:
        files = []
        for filename in os.listdir(directory):
            if extension and not filename.endswith(extension):
                continue
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                files.append({
                    "filename": filename,
                    "size": os.path.getsize(filepath),
                    "modified_date": datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
                })
        return files
    except Exception as e:
        return [{"status": "error", "message": str(e)}]

def write_file(filepath: str, content: str) -> dict:
    """
    Write content to a file, create directories if needed.
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return {"status": "success", "filepath": filepath}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def search_in_file(filepath: str, keyword: str) -> dict:
    """
    Search for a keyword in file content (case-insensitive).
    """
    try:
        result = read_file(filepath)
        if result["status"] != "success":
            return result

        content = result["content"].lower()
        keyword = keyword.lower()
        matches = []
        index = content.find(keyword)
        while index != -1:
            start = max(0, index - 30)
            end = min(len(content), index + len(keyword) + 30)
            snippet = result["content"][start:end]
            matches.append(snippet)
            index = content.find(keyword, index + 1)

        return {"status": "success", "count": len(matches), "matches": matches}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Quick test
if __name__ == "__main__":
    print(list_files("resumes"))  # show all files, not just .txt
