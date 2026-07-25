```markdown
#  Resume Assistant

A Python project that demonstrates **LLM tool calling** with structured file system tools.  
It can list resumes, read their contents, search for keywords, and generate summary files — all triggered by natural language queries.

---

##  Setup

1. Clone the repository or copy the project files.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Place 5–10 dummy resumes in the `resumes/` folder.  
   Supported formats: `.pdf`, `.docx`, `.txt`.


##  Project Structure

```
resume_assistant/
│
├── fs_tools.py              # Core file system tools
├── llm_file_assistant.py    # LLM integration dispatcher
├── requirements.txt         # Dependencies
├── resumes/                 # Sample resumes (PDF/DOCX/TXT)
├── summaries/               # Generated summary files
└── README.md                # Setup & usage instructions
```



## 🛠 Tools Implemented (fs_tools.py)

- **read_file** → Reads resume files, extracts text + metadata.
- **list_files** → Lists files in a directory, filters by extension.
- **write_file** → Writes content to file, creates directories if needed.
- **search_in_file** → Searches for keywords case‑insensitively, returns matches with context.


## LLM Integration (llm_file_assistant.py)

Natural queries are mapped to tool calls. Example queries:
- List all resumes
- Read all resumes in the resumes folder
- Find resumes mentioning Python experience
- Summarize Niveditha's resume
- Summarize Teja resume
- Summarize Hemanth resume
- Summarize all resumes with Java experience
- help → Lists supported queries.



## Usage

Run queries one by one from the command line:

```bash
python llm_file_assistant.py "List all resumes"
python llm_file_assistant.py "Read all resumes in the resumes folder"
python llm_file_assistant.py "Find resumes mentioning Python"
python llm_file_assistant.py "Summarize Niveditha's resume"
python llm_file_assistant.py "Summarize Teja resume"
python llm_file_assistant.py "Summarize Hemanth resume"
python llm_file_assistant.py "Summarize all resumes with Java experience"
python llm_file_assistant.py "help"
```

Each command triggers the correct tool call and prints results to the terminal.  
Summaries are saved in the `summaries/` folder.

---