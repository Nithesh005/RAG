# RAG Code Assistant

A simple tool to ask questions about your Python code using AI. For internal use only—everything is pre-set up.

## What It Does
- Scans Python files in a folder and saves info to a database.
- Lets you ask questions and get AI answers based on your code.

## Quick Start
1. Install stuff: `pip install psycopg2 sentence-transformers openai`
2. Run `python insert.py` and enter your project folder path (e.g., `C:\my-code`).
3. Run `python query.py` and type your question (e.g., "What does this function do?").

## Example
After scanning, ask: "Explain the User class" → Gets a smart answer from your code.

That's it! If something breaks, check Python and installs.