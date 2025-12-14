import re
# --------------UTILS----------------
import psycopg2
def get_conn():
    conn = psycopg2.connect(
        host="db.jxhtdnrmbasmwmbsjygm.supabase.co",       # e.g., "localhost" or an IP
        database="postgres", # e.g., "mydatabase"
        user="postgres",   # e.g., "postgres"
        password="1234", # your password
        port=5432               # default PostgreSQL port, change if needed
    )
    return conn

# ---------------- PARSERS ----------------
def parse_python_file(file_path):
    from sentence_transformers import SentenceTransformer, util
    model = SentenceTransformer("all-MiniLM-L6-v2")
    chunks = []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i]

        # Match class or function
        match = re.match(r"(\s*)(class|def)\s+(\w+)", line)
        if not match:
            i += 1
            continue

        indent = len(match.group(1))
        chunk_type = "class" if match.group(2) == "class" else "function"
        name = match.group(3)

        start_line = i + 1
        end_line = start_line

        j = i + 1
        while j < len(lines):
            next_line = lines[j]

            if next_line.strip() == "":
                j += 1
                continue

            next_indent = len(next_line) - len(next_line.lstrip())

            if next_indent <= indent:
                break

            end_line = j + 1
            j += 1

        source_text = "".join(lines[start_line - 1:end_line])
        chunks.append({
            "file": str(file_path),
            "start_line": start_line,
            "end_line": end_line,
            "type": chunk_type,
            "name": name,
            "source": source_text,
            "vectors": model.encode(source_text)
        })
        # print("embeding_length : ", len(chunks[-1]["vectors"]))

        i = j

    return chunks

def process_directory(directory: str):
    from pathlib import Path
    SUPPORTED_EXTENSIONS = {".py"}
    all_chunks = []
    for file_path in Path(directory).rglob("*"):
        if file_path.suffix not in SUPPORTED_EXTENSIONS:
            continue
        print("Processing file:", file_path)
        chunks = parse_python_file(file_path)

        for chunk in chunks:
            # chunk["class"] = classify_chunk(chunk)
            all_chunks.append(chunk)

    return all_chunks

# ---------------- INSERT IN DATABASE ----------------
def insert_embeddings(conn, data):
    from psycopg2.extras import execute_values
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS embeddings (
        id BIGSERIAL PRIMARY KEY,
        file TEXT,
        start_line INTEGER,
        end_line INTEGER,
        type TEXT,
        name TEXT,
        source TEXT,
        embedding VECTOR(384)
    );
    """

    query = """
    INSERT INTO embeddings (file, start_line, end_line, type, name, source, embedding)
    VALUES %s
    """
    values = [
        (
            item["file"],
            item["start_line"],
            item["end_line"],
            item["type"],
            item["name"],
            item["source"],
            item["vectors"].tolist()
        )
        for item in data
    ]

    if not values:
        return  # nothing to insert

    with conn:
        with conn.cursor() as cur:
            # Ensure table exists
            cur.execute(create_table_sql)
            cur.execute("TRUNCATE TABLE embeddings;") # Truncate the table before inserting
            execute_values(cur, query, values)



# ---------------- MAIN ----------------
if __name__ == "__main__":
    # source_dir = "D:\\Domain\\python\\OpenAI\\src"  # change this
    source_dir = input("Enter the directory path: ")
    results = process_directory(source_dir) # example : [{"file": "path/to/file.py", "start_line": 1, "end_line": 10, "type": "class", "name": "MyClass", "class": "class"}, ...]}]
    if not results:
        print("No chunks found in the directory.")
        exit()
    conn = get_conn()
    insert_embeddings(conn, results)