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

def handle_query(query: str):
    # Normalize query for fuzzy matching
    normalized_query = query.replace("'", "").replace("_", "").lower()

    # Help command
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

    # List resumes
    if "list" in normalized_query and "resume" in normalized_query:
        return fs_tools.list_files("resumes")

    # Read all resumes
    elif "read all resumes" in normalized_query:
        results = []
        for file in fs_tools.list_files("resumes"):
            results.append(fs_tools.read_file(f"resumes/{file['filename']}"))
        return results

    # Read a specific resume
    elif "read" in normalized_query:
        filename = query.split("read")[-1].strip()
        return fs_tools.read_file(f"resumes/{filename}")

    # Find resumes mentioning ANY keyword
    elif "find resumes mentioning" in normalized_query:
        keyword = normalized_query.split("mentioning")[-1].strip()
        results = []
        for file in fs_tools.list_files("resumes"):
            search_result = fs_tools.search_in_file(f"resumes/{file['filename']}", keyword)
            if search_result["count"] > 0:
                results.append({"filename": file["filename"], "matches": search_result["matches"]})
        return results

    # Summarize a specific resume by name or filename
    elif "create summary file for" in normalized_query or "create summary for" in normalized_query or "summarize" in normalized_query:
        filename = None

        # Try fuzzy name match (partial)
        for name, file in NAME_TO_FILE.items():
            if name in normalized_query:
                filename = file
                break

        # Fallback: check filenames directly
        if not filename:
            for file in fs_tools.list_files("resumes"):
                if any(word in file['filename'].lower() for word in normalized_query.split()):
                    filename = file['filename']
                    break

        # Final fallback: extract after 'for'
        if not filename and "for" in normalized_query:
            filename = query.split("for")[-1].strip()

        if filename:
            base_name = filename.replace(".pdf", "").replace(".docx", "")
            summary = f"Summary for {filename}: Candidate has strong skills."
            return fs_tools.write_file(f"summaries/{base_name}_summary.txt", summary)
        else:
            return {"status": "error", "message": "Could not identify resume name."}

    # Summarize all resumes with a given skill/keyword
    elif "summarize all resumes with" in normalized_query:
        keyword = normalized_query.split("with")[-1].strip()
        results = []
        for file in fs_tools.list_files("resumes"):
            search_result = fs_tools.search_in_file(f"resumes/{file['filename']}", keyword)
            if search_result["count"] > 0:
                base_name = file["filename"].replace(".pdf", "").replace(".docx", "")
                summary = f"Summary for {file['filename']}: Candidate has {keyword} experience."
                results.append(fs_tools.write_file(f"summaries/{base_name}_summary.txt", summary))
        return results

    else:
        return {"status": "error", "message": "Query not understood."}


if __name__ == "__main__":
    print(handle_query("help"))
    print(handle_query("List all resumes"))
    print(handle_query("Read all resumes in the resumes folder"))
    print(handle_query("Find resumes mentioning Python"))
    print(handle_query("Summarize Niveditha's resume"))
    print(handle_query("Summarize Teja resume"))
    print(handle_query("Summarize Hemanth resume"))
    print(handle_query("Summarize all resumes with Java experience"))
