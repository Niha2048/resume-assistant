import fs_tools

# Map simple names to actual filenames
NAME_TO_FILE = {
    "niveditha": "E_Niveditha_Resume (2).pdf",
    "erri teja": "Erri_Teja_Kumar_Resume (1).pdf",
    "hemanth": "Hemanth-Resume'U (1).pdf",
    "nirosha": "Nirosha_Erri_Java_S (1).pdf",
    "tejasri": "Tejasri_Java_Developer.pdf",
    "thejaswani": "Thejaswani_R_PMO_Resume_Updated-1 (1).docx"
}

def generate_summary(content: str, filename: str) -> str:
    """
    Extracts the full 'Summary' section from resume content.
    Captures all lines after 'Summary' until the next major section header.
    """
    lines = content.splitlines()
    summary_lines = []
    capture = False

    for line in lines:
        if "summary" in line.lower():
            capture = True
            continue
        if capture:
            # Stop when we hit another section header
            if any(header in line.lower() for header in ["work experience", "projects", "education", "skills"]):
                break
            if line.strip():
                summary_lines.append(line.strip())

    # Fallback if no summary section found
    if not summary_lines:
        summary_lines = ["Candidate resume content available."]

    summary_text = " ".join(summary_lines)
    return f"Summary for {filename}: {summary_text}"


def handle_query(query: str):
    normalized_query = query.replace("'", "").replace("_", "").lower()

    if "help" in normalized_query:
        return {
            "supported_queries": [
                "List all resumes",
                "Read all resumes",
                "Read <filename>",
                "Find resumes mentioning <keyword>",
                "Summarize <name>'s resume",
                "Summarize all resumes with <skill>"
            ]
        }

    if "list" in normalized_query and "resume" in normalized_query:
        return fs_tools.list_files("resumes")

    elif "read all resumes" in normalized_query:
        results = []
        for file in fs_tools.list_files("resumes"):
            results.append(fs_tools.read_file(f"resumes/{file['filename']}"))
        return results

    elif "read" in normalized_query:
        filename = query.split("read")[-1].strip()
        return fs_tools.read_file(f"resumes/{filename}")

    elif "find resumes mentioning" in normalized_query:
        keyword = normalized_query.split("mentioning")[-1].strip()
        results = []
        for file in fs_tools.list_files("resumes"):
            search_result = fs_tools.search_in_file(f"resumes/{file['filename']}", keyword)
            if search_result["count"] > 0:
                results.append({"filename": file["filename"], "matches": search_result["matches"]})
        return results

    elif "summarize" in normalized_query:
        filename = None
        for name, file in NAME_TO_FILE.items():
            if name in normalized_query:
                filename = file
                break

        if not filename:
            for file in fs_tools.list_files("resumes"):
                if any(word in file['filename'].lower() for word in normalized_query.split()):
                    filename = file['filename']
                    break

        if filename:
            file_content = fs_tools.read_file(f"resumes/{filename}")
            summary = generate_summary(file_content["content"], filename)
            base_name = filename.replace(".pdf", "").replace(".docx", "")
            fs_tools.write_file(f"summaries/{base_name}_summary.txt", summary)
            print(summary)  # <-- Print summary in terminal
            return {"status": "success", "message": f"Summary written to summaries/{base_name}_summary.txt"}
        else:
            return {"status": "error", "message": "Could not identify resume name."}

    elif "summarize all resumes with" in normalized_query:
        keyword = normalized_query.split("with")[-1].strip()
        results = []
        for file in fs_tools.list_files("resumes"):
            search_result = fs_tools.search_in_file(f"resumes/{file['filename']}", keyword)
            if search_result["count"] > 0:
                file_content = fs_tools.read_file(f"resumes/{file['filename']}")
                summary = generate_summary(file_content["content"], file['filename'])
                base_name = file["filename"].replace(".pdf", "").replace(".docx", "")
                fs_tools.write_file(f"summaries/{base_name}_summary.txt", summary)
                print(summary)  # <-- Print each summary in terminal
                results.append({"status": "success", "file": base_name})
        return results

    else:
        return {"status": "error", "message": "Query not understood."}


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python llm_file_assistant.py '<query>'")
    else:
        query = sys.argv[1]
        result = handle_query(query)
        print(result)
