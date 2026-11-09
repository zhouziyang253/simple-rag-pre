from src.embedding.func_embedding import func_embedding
from sentence_transformers import util
import pickle
import torch


query = "今天你心情怎么样？"
query_chunk = [query]
query_vector = func_embedding(query_chunk)
# print(query)
#使用pickle转码文件到一个 列表【字典】，内部的最小结构是{id:...,vector:...,text:...,location:...}
with open("vector_db.pkl","rb") as f:
    info_db = pickle.load(f)

vector_db = []
for info in info_db:
    vector_db.append(info["vector"])

answer_matrix = util.cos_sim(query_vector,vector_db)
print(answer_matrix)
answer_texts = []
print(answer_matrix[0].shape)
#获得最大的那个序号的索引 %%%这里之后可能需要修改为一个返回前几个值
# for i in range(len(query_chunk)):
#     answer_text_i =[]
#     index = 0
#     maxnum = answer_matrix[i][0]
#     for j in range(len(answer_matrix[i])):
#         print(info_db[j]["text"])
#         if answer_matrix[i][j] > maxnum:
#             index = j
#             maxnum = answer_matrix[i][j]
#     #这是对第i个问题的chunks最初回答文本的收集
#     answer_text_i.append(info_db[index]["text"])
#     #最后汇总到一个二维数组
#     answer_texts.append(answer_text_i)
# print(answer_texts)

#可以使用torch的处理方式来获得前几大的数值 topk返回（数值，索引）
for i in range(len(query_chunk)):
    answer_text_i =[] #第i个query的文本回答
    # 这里的index_i是一个二维数组，其中第一个量是1，表示一维（在iquery上的）；然后把第二个量的唯独就是答案对应的索引
    _ , index_i = torch.topk(answer_matrix[i,:],k=2) #针对地i个query块的最佳匹配的索引

    for j in index_i:
        answer_text_i.append(info_db[j]["text"])
    answer_texts.append(answer_text_i)
print(answer_texts)
    