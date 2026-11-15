- (11.8)这是我第一次尝试手写RAG，感觉非常的困难。

- (11.9)这两天完成了embedding vectordb retrival 的demo，然后今天看到陈家航学长的朋友圈感触颇深。感觉AI的出现确实减少了很多的代码创作的快乐。好在这个项目只是个人的练手，AI只是起到一个检索和查询的功能，所以写起来倒还是挺轻松的。主要是感觉自己又掌握了更多的知识。
    -具体来说今天主要是学习了这些内容：
     - with open() as:
     - pickle
     - similarity -> util.cos_sim()分析接近程度，embedding记得normalize_embedding=True
     - topk 返回（x，index） 最大的k个
     - if ____name____ == "____main____": 以及断点测试
- 之后继续完成这个demo，然后有条件可以修改一下func_answer_info,返回的字典里面加上query chunks,不加也没事，之后也prompt时候注意一下

- (11.11)现在已经完成了第一版，可以在pkl文件生成之后使用大模型在检索增强的功能下使用。默认的环境配置是：
    - ollama提供本地服务
    - 默认采用qwen3.5:9b
    - 仍然采用pkl+load的存储使用方式
    - Embedding模型采用的是'BAAI/bge-m3'，这个模型直接连接并不稳定，需要先下载到本地。或许可以采用其他的Embedding模型进行测试。
- 如果需要使用，请提前安装好以下库：
    - sentence-transformer
    - pickle
    - pathlib
    - openai
- 具体使用的步骤如下：
    1. 第一次使用时请确保ollama服务正常开启，确保ollama服务之中有qwen3.5:9b这个模型（如果没有，第一次使用会自动拉取，但是速度会比较慢）
    2. 将检索文件放入data文件夹 (目前已知支持txt文件，应该是utf-8编码的文件都没有问题)
    3. 进入程序后首先进入src/vector_db/func_write_in运行(ctrl+f5,终端运行)
    4. 待data_vector中生成文件之后，打开主程序main.py,运行（ctrl+f5,终端运行）
    5. 在终端窗口按照提示输入问题，等待一段时间(通常是60s-120s)
- 注意这里只有标注是func_开头的文件是函数所在，其余的python文件是测试时用的，部分已经不能正常使用。
-  本次修改的收获  
感受上来说：行百里者半九十吧，到后面真的不能着急，后面的调整感觉很困难，不会比前面创作轻松；  
知识上来说：一个是把这种模型，大的文件写到函数的参数，而不是函数内部，防止多次调用函数导致模型、大文件反复加载。之后只需要在调用函数时把这个文件和模型写在外面。再一个是使用pathib可以寻找、创造文件夹，这个挺方便的。最后就是先写能跑的，然后封装，最后再调整。
- 后续的修改方案：
    1. 把文件写入func_write_in写入主程序main.py，一键化
    2. 使用标准的数据库(chromadb之类的)加快运行速度
    3. 调整提示词，让这个提示词变得更加合适
    4. 使用流式输出
    5. 写上接入云端模型的方法，并且加上本地模型的修改部分
    6. 加上前端

- （11.15）回顾代码，之后先加上图像处理模型，基本思路是多写几个额外的函数，将这个图片转化为一个文本描述，这样就可以了。具体的数据流动应该是这样的:

    - 配置好环境（需要指定工作目录，这个在.vscode里面做到了；需要在外面加载大模型以及对应的client）
    
    -  func_getlocations（输入文件夹路径，扫描文件夹中的文件（list[str]））->获得一个文件夹中间的所有文件路径locations:list[str]
    -> func_get_text.get_row(locations)（一个文件）-> 扫描文本（txt等，utf-8编码），进行按行划分（这只是针对一个文件）-> 一个文本的划分rows：list[str] ->func_get_text.max_num_chunks(MAXNUM，chunks) ->对行进行组合处理，变成一个一个chunks：list[str]

    ->func_vectordic(locations:list[str],embeddingmodel)->list[dict],这是将一个地方的所有的文本转化到embedding向量的方法，使用到了前面的get_rows,max_num_chunks 
    ->func_write_in(locations,embedidngmodel) 这里在func_vectordic上面加上点，加上写入的步骤（with open () as f:pkl），将这些list[str]转化为pkl存起来（存在默认文件夹data_vector）
    （注意个写入操作只需要进行一次就好了，这个也是在启动主程序之前做的）

    ->func_answer_info.answer_info(),这里需要使用问题的embedding向量，因此在主程序调用时需要一个func_embedding(),然后输入问题、知识库的embedding vector之后就可以使用cos_sim分析近似度，使用topk找到需要的内容
    ->func_getanswer就是将这些文本（prompt，以及资料库放入模型之中（注意这里其实不是直接交给模型处理，而是需要先经过ollama帮忙，本质上是链接一个类似APIkey的的东西）） ->获得答案

    最好不要把模型，大文件等显性的作为函数的参数传入（就是指在def的时候），因为这样的话，每次import这个函数的时候就会自动做一次传入初始化。这个时候这个参数应该留空，在函数使用前面定义会更好。（____main____）