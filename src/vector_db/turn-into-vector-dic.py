from src.cutting.func_get_text import max_num_chunks,get_row
from src.embedding.func_embedding import func_embedding
location = "/home/mike/simple-rag-pre/data/first.txt"
rows = get_row(location)
chunks = max_num_chunks(MAX_NUM=20,rows=rows)
embeddings = func_embedding(chunks=chunks)
# print(embeddings)

info = []
# single_info = {”id“:id(embedding),"vector":embedding,"原文":chunk,"出处":location}
for i in range(len(chunks)):
    single_info = {"id":id(embeddings[i]),
                   "vector":embeddings[i],
                   "text":chunks[i],
                   "location":location}
    info.append(single_info)
print(info)