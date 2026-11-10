from src.embedding.func_embedding import func_embedding
from sentence_transformers import util
import pickle
import torch

def answer_info(query_vector:list,info_db:list[dict],top_k = 5)->list[list[dict]]:
    '''输入一个问题的embedding向量以及资料库info_db,
    输出一个新的answer_db,为list[list[dict]]类型,
    其中第一层表示针对不同的query chunks,第二层针对每一个问题返回的chunks块的信息,
    每个块以dict形式保存["id":...,"vector":...,"text":...,"location":...]'''
    vector_db = []
    for info in info_db:
        vector_db.append(info["vector"])
    
    answer_matrix = util.cos_sim(query_vector,vector_db)
    # print(answer_matrix)
    answer_info = []

    #可以使用torch的处理方式来获得前几大的数值 topk返回（数值，索引）
    for i in range(len(query_vector)):
        answer_text_i =[] #第i个query的文本回答
        # 这里的index_i是一个二维数组，其中第一个量是1，表示一维（在iquery上的）；然后把第二个量的唯独就是答案对应的索引
        _ , index_i = torch.topk(answer_matrix[i,:],k=top_k) #针对地i个query块的最佳匹配的索引
    
        for j in index_i:
            answer_text_i.append(info_db[j])
        answer_info.append(answer_text_i)
    return answer_info

if __name__ == "__main__":
    # query = "今天你心情怎么样？"
    query_chunk = ["今天你心情怎么样？","怎么用英文打招呼"]
    query_vector = func_embedding(query_chunk)
    # print(query)
    #使用pickle转码文件到一个 列表【字典】，内部的最小结构是{id:...,vector:...,text:...,location:...}
    with open("vector_db.pkl","rb") as f:
        info_db = pickle.load(f)
    answer_list = answer_info(query_vector=query_vector,info_db=info_db)
    for i,answer in enumerate(answer_list):
        print(f"This is the {i} of the chunks.")
        for single in answer:
            print(single["id"])
            print(single["location"])
            print(f"{single["text"]}\n")