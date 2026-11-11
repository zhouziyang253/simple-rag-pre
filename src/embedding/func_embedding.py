from sentence_transformers import SentenceTransformer
import numpy as np

#使用chunks（语言块）对应到向量embedding
#embeddingmodel=SentenceTransformer('BAAI/bge-m3',revision='main',local_files_only=True)
def func_embedding(chunks,embeddingmodel): # 使用main分支，下载之后直接指定使用本地模型)->np.ndarray
    #向量化
    embeddings = embeddingmodel.encode(chunks,batch_size=5,show_progress_bar=True,normalize_embeddings=True)
    return embeddings