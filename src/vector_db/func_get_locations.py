from pathlib import Path

def func_get_locations(folder:str="data")->list[str]:
    '''输入一个文件夹，返回其中文件的路径'''
    folder = Path(folder)
    locations = []
    for file in folder.iterdir():
        locations.append(f"{folder}/{file.name}")
    return locations

if __name__ == "__main__":
    print(func_get_locations("data"))