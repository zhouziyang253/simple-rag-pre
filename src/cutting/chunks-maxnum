import re

with open("/home/mike/simple-rag-pre/data/first.txt",encoding="utf-8") as f :
    text = f.read() ##将这个读取对象以字符串的形式
    rows = text.split('\n') ##split可以按照这个一个标点切分。就是拿文本切成一行一行
    row_parts = [] ##这是创建一个二位数组，把一行中间再按照需要的符号切开，然后同一行的在同一个数组里面，不同行又构成第二个维度
    for row in rows :
        parts_temp = re.split(r"[,.'\"\\:;!？‘’；：！]+",row)
        parts = []
        for p in parts_temp:
            if p !='':
                parts.append(p)
        row_parts.append(parts)

# 使用rows似乎比使用row_parts更有效
chunks =[]
MAXNUM = 20
temp_str = ''

for row in rows :
    if len(temp_str)+len(row)<MAXNUM:
        temp_str += row
    else:
        chunks.append(temp_str)
        temp_str = row
chunks.append(temp_str)
print(chunks)
