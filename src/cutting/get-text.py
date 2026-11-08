import re
##这里使用with open（） as的好处是不需要关闭，自动关闭
with open("/home/mike/simple-rag-pre/data/first.txt",encoding="utf-8") as f :
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
print(row_parts)
