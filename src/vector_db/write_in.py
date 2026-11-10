from src.vector_db.func_vectordic import func_vectordic
import pickle #转换到二进制里面去了,保存更加方便

locations=["/home/mike/simple-rag-pre/data/coding_test.txt"]
info_dict = func_vectordic(locations=locations)
print(info_dict)
with open("vector_db_test.pkl","wb") as f:
    pickle.dump(info_dict,f)
