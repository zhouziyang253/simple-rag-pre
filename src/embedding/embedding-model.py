from src.cutting.func_get_text import max_num_chunks,get_row
from sentence_transformers import SentenceTransformer

#处理文本为一个个chunks
str0 = "/home/mike/simple-rag-pre/data/first.txt"
rows = get_row(str0)
chunks = max_num_chunks(MAX_NUM=20,rows=rows)

#加载模型
model = SentenceTransformer('BAAI/bge-m3',revision='main',local_files_only=True) #使用main分支，下载之后直接指定使用本地模型

#向量化
embeddings = model.encode(chunks,batch_size=5,show_progress_bar=True)
print(chunks)
print(type(embeddings))
print(embeddings.shape)
print(embeddings)
#similarity