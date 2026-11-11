from openai import OpenAI
from src.embedding.func_embedding import func_embedding
import pickle
from src.retrival.func_answer_info import answer_info
from sentence_transformers import SentenceTransformer
def func_getanswer(query,client,embedding_model,source:str ="data_vector/vector_db_test.pkl",
                   model_name="qwen3.5-16k:latest"):
    '''输入一个问题，在指定数据库和指定模型后，输出一个回答(一个很大的东西openai.types.chat.chat_completion.ChatCompletion)'''

    query_chunk = [query]
    query_vector = func_embedding(query_chunk,embeddingmodel=embedding_model)
    # print(query)
#使用pickle转码文件到一个 列表【字典】，内部的最小结构是{id:...,vector:...,text:...,location:...}
    with open(source,"rb") as f:
        info_db = pickle.load(f)
    answer_list = answer_info(query_vector=query_vector,info_db=info_db)

# print("I have find the related text.")
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
            {"role":"system","content":"You are a responsible AI. Your answer is concise. The question you meet is about coding,so you must notice your format and spelling. And you will not generate something you don't know.Reply in the same language the question use."},
            {"role":"user","content":f"Here is my question: {query},and the reliable source is {answer_text}."},
        ],
        reasoning_effort="none"
        )
    return response
    # u = response.usage
    # print(f"input tokens:{u.prompt_tokens}")
    # print(f"complete tokens:{u.completion_tokens}")
    # print(f"total tokens:{u.total_tokens}")

if __name__=="__main__":
    client= OpenAI(
        base_url= "http://localhost:11434/v1",
        api_key= "ollama")
    query = input ("Please input the question:\n")
    embeddingmodel=SentenceTransformer('BAAI/bge-m3',revision='main',local_files_only=True)
    response = func_getanswer(query=query,client=client,embedding_model=embeddingmodel)
    print(response.choices[0].message.content)
    print(response.usage.completion_tokens)
    print(response.usage.prompt_tokens)
    print(response.usage.total_tokens)