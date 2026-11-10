from src.cutting.func_get_text import max_num_chunks,get_row
from src.embedding.func_embedding import func_embedding


def func_vectordic(locations:list[str])->list[dict]:
    info = []
    for location in locations:
        rows = get_row(location)
        chunks = max_num_chunks(MAX_NUM=50,rows=rows)
        embeddings = func_embedding(chunks=chunks)
        # single_info = {”id“:id(embedding),"vector":embedding,"原文":chunk,"出处":location}
        for i in range(len(chunks)):
            single_info = {"id":id(embeddings[i]),
                           "vector":embeddings[i],
                           "text":chunks[i],
                           "location":location}
            info.append(single_info) #这只是一个location的数据dict
    return info ##这个就是所有的locations对应的字典
        
#test
# if __name__=="__main__":
#     locations=["/home/mike/simple-rag-pre/data/first.txt"]
#     info_dict = func_vectordic(locations=locations)
#     print(info_dict)