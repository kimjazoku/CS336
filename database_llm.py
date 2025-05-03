import os
import getpass
import paramiko
from llama_cpp import Llama

# === CONFIG ===
MODEL_PATH = r"C:\Users\Unreal\Downloads\model\Phi-3.5-mini-instruct-Q4_K_M.gguf"  # <-- Adjust this path to fit wherever u installed the llm
SCHEMA_FILE = "schema.sql"  # Optional: put your CREATE TABLE statements here
ILAB_USER = input("Enter your iLab NetID: ")
ILAB_HOST = "ilab.rutgers.edu"  # or specific node name
REMOTE_SCRIPT_PATH = "~/proj2/ilab_script.py"  # Adjust this to the full path on ILAB
CTX_LEN = 2048
MAX_TOKENS = 200


# === LOAD SCHEMA ===
def load_schema():
    if os.path.exists(SCHEMA_FILE):
        with open(SCHEMA_FILE, "r") as file:
            return file.read()
    else:
        print(f"ERROR: Schema file '{SCHEMA_FILE}' not found. Please create it and include CREATE TABLE statements.")
        exit(1)


# === LOAD LLM ===
def load_model():
    print("Loading model...")
    llm = Llama(model_path=MODEL_PATH, n_ctx=CTX_LEN)
    print("Model loaded.\n")
    return llm


# === GENERATE SQL ===
def generate_sql(llm, schema_text, user_question):
    prompt = f"""
You are a helpful SQL assistant. Write a SQL SELECT query based on the schema and question.

### SCHEMA:
{schema_text}

### QUESTION:
{user_question}

### SQL:
"""
    output = llm(prompt, max_tokens=MAX_TOKENS)
    response = output["choices"][0]["text"].strip()

    if not response.lower().startswith("select"):
        response = "SELECT " + response.lstrip()

    return response + ";"


# === SSH & EXECUTE REMOTE QUERY ===
def run_query_on_ilab(sql_query):
    ssh_password = getpass.getpass(f"Enter SSH password for {ILAB_USER}@{ILAB_HOST}: ")

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ILAB_HOST, username=ILAB_USER, password=ssh_password)

        safe_query = sql_query.replace('"', '\\"')
        remote_cmd = f'python3 {REMOTE_SCRIPT_PATH} "{safe_query}"'
        stdin, stdout, stderr = client.exec_command(remote_cmd)

        output = stdout.read().decode()
        error = stderr.read().decode()

        print("\n=== Query Result ===")
        print(output)
        if error:
            print("=== Errors ===")
            print(error)

        client.close()

    except Exception as e:
        print(f"SSH error: {e}")


# === MAIN PROGRAM ===
def main():
    schema_text = load_schema()
    llm = load_model()

    while True:
        user_question = input("\nAsk a database question (or type 'exit'): ").strip()
        if user_question.lower() == "exit":
            break

        sql_query = generate_sql(llm, schema_text, user_question)
        print("\nGenerated SQL Query:")
        print(sql_query)

        run_query_on_ilab(sql_query)


if __name__ == "__main__":
    main()
