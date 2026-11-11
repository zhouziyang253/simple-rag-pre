from openai import OpenAI
from src.retrival.func_answer_info import answer_info
from src.embedding.func_embedding import func_embedding
import pickle

client = OpenAI(
    base_url= "http://localhost:11434/v1",
    api_key= "ollama"
)
model_name = "qwen3.5:9b"

query_input = input("Please input the question:\n")
query_chunk = [query_input]
query_vector = func_embedding(query_chunk)
# print(query)
#使用pickle转码文件到一个 列表【字典】，内部的最小结构是{id:...,vector:...,text:...,location:...}
with open("vector_db_test.pkl","rb") as f:
    info_db = pickle.load(f)
answer_list = answer_info(query_vector=query_vector,info_db=info_db)

print("I have find the related text.")
answer_text = []
for i,answer in enumerate(answer_list):
    # print(f"This is the {i} of the chunks.")
    for single in answer:
        answer_text.append(single["text"])
        # print(single["id"])
        # print(single["location"])
        # print(f"{single["text"]}\n")

# print(f"Here is my question: {query_input},and the reliable source is {answer_text}.")
response = client.chat.completions.create(
    model= model_name,
    messages=[
        {"role":"system","content":"You are a responsible AI. The question you meet is about coding,so you must notice your format and spelling. And you will not generate something you don't know."},
        {"role":"user","content":f"Here is my question: {query_input},and the reliable source is {answer_text}."},
    ],
    reasoning_effort="none"

)
print(response.choices[0].message.content)
u = response.usage
print(f"input tokens:{u.prompt_tokens}")
print(f"complete tokens:{u.completion_tokens}")
print(f"total tokens:{u.total_tokens}")
print(type(response))