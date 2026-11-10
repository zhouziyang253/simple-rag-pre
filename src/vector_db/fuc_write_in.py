from src.vector_db.func_vectordic import func_vectordic
import pickle #转换到二进制里面去了,保存更加方便
from pathlib import Path

def func_write_in(locations:list[str]) ->None :
    """执行写入操作"""
    info_dict = func_vectordic(locations=locations)
    Path("data_vector").mkdir(parents=True,exist_ok=True) #便于创建多级文件；不必在文件是否存在
    with open("data_vector/vector_db_test.pkl","wb") as f:
        pickle.dump(info_dict,f)

if __name__ == "__main__":
    func_write_in(["/home/mike/simple-rag-pre/data/coding_test.txt"])
