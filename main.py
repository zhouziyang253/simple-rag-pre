import pickle
from sentence_transformers import SentenceTransformer
from src.answer.func_getanswer import func_getanswer
from openai import OpenAI
from src.vector_db.fuc_write_in import func_get_locations,func_write_in

def main(info_db,vector_db,client,embeddingmodel):
        state = 'y'
        while(state != 'n'):
                query = input ("Please input the question:\n")        
                response = func_getanswer(query=query,client=client,embedding_model=embeddingmodel,info_db=info_db,vector_db=vector_db)
                print(response.choices[0].message.content)
                print(f"output tokens:{response.usage.completion_tokens}")
                print(f"input Tokens:{response.usage.prompt_tokens}")
                print(f"Toltal Tokens:{response.usage.total_tokens}")
                state = input("Do you want to ask question more? 'y'/'n':")

if __name__ == "__main__":
#    update_state =input("Do you need to update the knowledge base? y/n: ")
#     if update_state=='y':
#         locations = func_get_locations("data")
#         func_write_in(locations=locations,
#                           embeddingmodel=SentenceTransformer('BAAI/bge-m3',revision='main',local_files_only=True))
    
    client = OpenAI(
            base_url= "http://localhost:11434/v1",
            api_key= "ollama")
    embeddingmodel = SentenceTransformer('BAAI/bge-m3',revision='main',local_files_only=True)
    update_state =input("Do you need to update the knowledge base? y/n: ")
    if update_state=='y':
                locations = func_get_locations("data")
                func_write_in(locations=locations,
                          embeddingmodel=embeddingmodel)
    else:
        locations = func_get_locations("data_vector")
        if not locations:
                raise FileNotFoundError("The currnet knowledge base is empty, please initialize first.")
    with open("data_vector/vector_db_test.pkl","rb") as f:
             info_db = pickle.load(f)
    vector_db =[]
    for info in info_db:
            vector_db.append(info["vector"])
    
    main(info_db=info_db,vector_db=vector_db,client=client,embeddingmodel=embeddingmodel)