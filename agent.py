from langchain.chains import LLMChain
from langchain_community.llms import Ollama
from prompt_template import db_prompt
import json
import os

# Use the locally running LLaMA 2 model from Ollama
llm = Ollama(model="llama2")  # You can change to "mistral" or "phi3" if needed

# Load the column_directory.json
with open(os.path.join(os.path.dirname(__file__), 'column_directory.json')) as f:
    column_synonyms = json.load(f)

# Function to replace synonyms in the prompt
def replace_synonyms(question, synonym_dict):
    for phrase, actual in synonym_dict.items():
        question = question.replace(phrase, actual)
    return question

def generate_query(user_question):
    cleaned_question = replace_synonyms(user_question.lower(), column_synonyms)
    print("Processed prompt:", cleaned_question)

    chain = LLMChain(llm=llm, prompt=db_prompt)
    sql_query = chain.run(question=cleaned_question).strip()

    print("Generated SQL:", sql_query)

    if not sql_query.lower().startswith(("select", "insert", "update", "delete")):
        raise ValueError("Generated query is not a valid SQL statement.")

    return sql_query
