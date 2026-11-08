import re

def get_row(str0)->list[str]:
    '''给出路径，用来返回文本切为行的字符串列表'''
    with open(str0,encoding="utf-8") as f:
        text = f.read() ##将这个读取对象以字符串的形式
        rows = text.split('\n') ##split可以按照这个一个标点切分。就是拿稳本切成一行一行
    return rows

def get_text(str0)->list[list[str]]:
    '''给出路径，用来返回文本切为行之内的一句话的最小情况的二位列表'''
    with open(str0,encoding="utf-8") as f:
        text = f.read() ##将这个读取对象以字符串的形式
        rows = text.split('\n') ##split可以按照这个一个标点切分。就是拿稳本切成一行一行
        row_parts = [] ##这是创建一个二位数组，把一行中间再按照需要的符号切开，然后同一行的在同一个数组里面，不同行又构成第二个维度
        for row in rows :
            parts_temp = re.split(r"[,.'\"\\:;!？‘’；：！]+",row)
            parts = []
            for p in parts_temp:
                if p !='':
                    parts.append(p)
            row_parts.append(parts)
    return row_parts

def max_num_chunks(MAX_NUM,rows)->list[str]:
    chunks =[]
    temp_str = ''
    for row in rows :
        if len(temp_str)+len(row)<MAX_NUM:
            temp_str += row
        else:
            chunks.append(temp_str)
            temp_str = row
    chunks.append(temp_str)
    return chunks
    


if __name__ == "__main__":
    rows = get_row("/home/mike/simple-rag-pre/data/first.txt")
    chunks =max_num_chunks(20,rows)
    print(chunks)