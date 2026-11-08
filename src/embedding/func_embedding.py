from sentence_transformers import SentenceTransformer
import numpy as np

#使用chunks（语言块）对应到向量embedding
def func_embedding(chunks)->np.ndarray:
    model = SentenceTransformer('BAAI/bge-m3',revision='main',local_files_only=True) #使用main分支，下载之后直接指定使用本地模型
    #向量化
    embeddings = model.encode(chunks,batch_size=5,show_progress_bar=True)
    return embeddings