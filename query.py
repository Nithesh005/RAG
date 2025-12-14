from openai import OpenAI

key = "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"
client = OpenAI(api_key= key)

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



def raw_question_to_vector(question):
    from sentence_transformers import SentenceTransformer, util
    model = SentenceTransformer("all-MiniLM-L6-v2")
    vector_question = model.encode(question)
    return vector_question

def table_exists(conn, table_name, schema="public"):
    query = """
    SELECT EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = %s
          AND table_name = %s
    );
    """
    with conn.cursor() as cur:
        cur.execute(query, (schema, table_name))
        return cur.fetchone()[0]

def search_embeddings(conn, vector, top_k):
    # ✅ convert numpy array → python list
    if hasattr(vector, "tolist"):
        vector = vector.tolist()

    if not table_exists(conn, "embeddings"):
        # decide how you want to handle this case
        return []  
    
    query = """
    SELECT file, start_line, end_line, type, name, source
    FROM embeddings
    ORDER BY embedding <=> %s::vector
    LIMIT %s;
    """

    with conn.cursor() as cur:
        cur.execute(query, (vector, top_k))
        return cur.fetchall()


# ---------------- ASK LLM ----------------
def get_answer_from_llm(client, information, question):
    prompt = f"""
        You are an assistant. Use the following information to answer the question.
        Information: "{information}"
        Question: "{question}"

        Give me smart answer short and simple.
    """
    print("Prompt sent to model:")
    print(prompt)
    
    response = client.responses.create(
        model="gpt-5-nano",
        input=prompt,
        store=True,
    )
    
    return response.output_text

if __name__ == "__main__":
    question = input("Enter your question: ")
    conn = get_conn()
    print("Vectorizing question...")
    vector_question = raw_question_to_vector(question) # Change this human readable to vector
    results = search_embeddings(conn, vector_question, 1)
    if len(results) == 0:
        print("1st step to intiate insert.py --> to run this file")
        exit()
    information = []
    meta_data = []
    for item in results:
        information.append(item[5])

        # Extract meta_data (indices 1, 2, 4)
        source_info = {
            "file_location": item[0],
            "start_line": item[1],
            "name": item[4]
            # "end_line": item[2],
        }
        meta_data.append(source_info)

    answer = get_answer_from_llm(client, information, question)
    # print("information:", information)
    print("answer :", answer)
    print("meta_data:", meta_data)

    