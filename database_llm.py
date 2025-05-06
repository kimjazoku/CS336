import os
import getpass
import re
import paramiko
from llama_cpp import Llama

# to execute: .\llm_env\Scripts\Activate.ps1
# then: python database_llm.py


# === CONFIG ===
MODEL_PATH = r"C:\Users\Unreal\Downloads\models\Phi-3.5-mini-instruct-Q4_K_M.gguf"  # <-- Adjust this path to fit wherever u installed the llm
SCHEMA_FILE = "schema.sql"  # Optional: put your CREATE TABLE statements here
ILAB_USER = input("Enter your iLab NetID: ")
ILAB_HOST = "cpp.cs.rutgers.edu"  # or specific node name
REMOTE_SCRIPT_PATH = "/common/home/jgk98/Desktop/300_Level/CS336/Proj2/ilab_script.py"  # <-- Adjust this to the full path on ILAB
CTX_LEN = 2200
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
You are a SQL generation assistant.  
Output **only** a single valid `SELECT` query (no markdown, no commentary), ending with a semicolon.
When querying tables denial_reason and race, remember there is two tables that seperate the name, and its id/num (to application)

=== BEGIN SCHEMA ===
{schema_text}
=== END SCHEMA ===

=== BEGIN EXAMPLES ===
Q: What is the average applicant income?
A: SELECT AVG(applicant_income_000s) FROM applications;
=== END EXAMPLES ===

=== BEGIN QUESTION ===
{user_question}
=== END QUESTION ===

A:

"""
    output = llm(prompt, max_tokens=MAX_TOKENS)
    response = output["choices"][0]["text"].strip()

    if not response.lower().startswith("select"):
        response = "SELECT " + response.lstrip()

    return response


def clean_response(text):
    text = re.sub(r"```(?:sql)?\n.*?```", "", text, flags=re.DOTALL | re.IGNORECASE).strip()
    first_select = re.search(r"(SELECT .*?;)", text, re.DOTALL | re.IGNORECASE)
    if first_select:
        return first_select.group(1).strip()
    
    # Fallback: Return original text (will error later if not a valid query)
    return text.strip()

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
        parsed_query = clean_response(sql_query)
        run_query_on_ilab(parsed_query)


if __name__ == "__main__":
    main()

# example question
# How many mortgages have a loan value greater than the applicant income?
# What is the average income of owner occupied applications?
# What is the most common loan denial reason?
