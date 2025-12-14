# Beginner-Friendly Guide to RAG Code Assistant

Welcome! This project is a simple Retrieval-Augmented Generation (RAG) system that helps you ask questions about Python code in a directory. It uses AI to understand and answer queries based on your code.

## What It Does
- **insert.py**: Scans a folder of Python files, extracts classes and functions, and stores them in a database with AI embeddings.
- **query.py**: Lets you ask questions about the code, finds relevant parts, and gives smart answers using AI.

## Prerequisites
- Python 3.8 or higher installed on your computer.
- A PostgreSQL database (we use Supabase, a free cloud option).
- Internet connection for AI models.

## Setup
1. **Install Dependencies**:
   Open a terminal (like PowerShell on Windows) and run:
   ```
   pip install psycopg2 sentence-transformers openai
   ```

2. **Database Setup**:
   - Sign up for a free Supabase account at [supabase.com](https://supabase.com).
   - Create a new project and get your database connection details (host, user, password).
   - Update the `get_conn()` function in both `insert.py` and `query.py` with your details (replace the example values).

3. **OpenAI API Key**:
   - Get an API key from [OpenAI](https://platform.openai.com/api-keys).
   - Update the `key` variable in `query.py` with your key.

## How to Use
1. **Prepare Your Code**:
   - Put your Python project files in a folder (e.g., `C:\my-python-project`).

2. **Run insert.py**:
   - Open a terminal in this project folder (`d:\Domain\python\RAG`).
   - Run: `python insert.py`
   - When prompted, enter the full path to your Python project folder (e.g., `C:\my-python-project`).
   - Wait for it to process and store the code in the database.

3. **Run query.py**:
   - In the same terminal, run: `python query.py`
   - When prompted, type your question about the code (e.g., "What does the main function do?").
   - Get an AI-powered answer based on your code!

## Example
- After running insert.py on a folder with Python files, ask: "Explain the class User."
- The system will find relevant code snippets and explain them.

## Troubleshooting
- If you get database errors, double-check your Supabase connection details.
- For OpenAI errors, ensure your API key is correct and you have credits.
- Make sure all dependencies are installed.

Have fun exploring your code with AI!