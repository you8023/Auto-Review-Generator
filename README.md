# Auto-Review-Generator自动综述生成器
Read and translate English literature to generate review automatically

github上图片可能无法查看，完整教程见[博客](https://www.jianshu.com/p/3639aac9d520)

如果不想了解技术细节，只想直接拿来用，可以直接跳过代码编写部分，直达最后代码使用部分。

**本代码免费[开源](https://github.com/you8023/Auto-Review-Generator)，如果你觉得好用，希望能够给我一个Star，也欢迎去[github](https://github.com/you8023/Auto-Review-Generator/issues)发表意见建议。**

代码实现效果如下：
![实现效果](https://upload-images.jianshu.io/upload_images/5714082-308ebb2f869973a9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 开发环境
* Windows 10
* Sublime Text 3
* Python 3.7
* Pdfminer
* 有道翻译API

## 事前准备
### 接口申请
本代码使用了有道翻译的API，因此，如需使用，需要去有道翻译接口官方申请APP Key和Secret key，直接按照其[官方教程](https://ai.youdao.com/doc.s#guide)申请即可，后续需要在代码中配置。接口申请完全免费，初始会送100元的面值，用完需要续费，不过一般情况100元可以用很久了。
### 安装pdfminer
因为我使用的是python3，因此输入以下命令安装：
```shell
pip install pdfminer4k
```
### 需求分析
这里分析了本代码实现的关键点：
* 文献是已经下载下来的pdf文件
* 文献中，需要提取的部分主要为：
  * 标题
  * 作者
  * 摘要
  * 结论

因此，本代码的思路是读取本地文件夹内的pdf文件，然后读取并识别出其关键元素，调用有道翻译的API进行翻译，并进行有机组合，写入TXT文件中。
## 代码编写
### 读取pdf文件
依次读取文件夹内的文件，如果后缀为pdf，则写入文件元祖：
```python
def getFileName(filepath):
    file_list = []
    for root,dirs,files in os.walk(filepath):
        for filespath in files:
            if 'pdf' in filespath.split('.')[1]:
                file_list.append(os.path.join(root,filespath))
    return file_list
```
### 读取文件内容并提取标题、作者、摘要和结论
```python
def parse(DataIO, save_path, appKey, appSecret):
 
    #用文件对象创建一个PDF文档分析器
    parser = PDFParser(DataIO)
    #创建一个PDF文档
    doc = PDFDocument()
    #分析器和文档相互连接
    parser.set_document(doc)
    doc.set_parser(parser)
    #提供初始化密码，没有默认为空
    doc.initialize()
    #检查文档是否可以转成TXT，如果不可以就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        #创建PDF资源管理器，来管理共享资源
        rsrcmagr = PDFResourceManager()
        #创建一个PDF设备对象
        laparams = LAParams()
        #将资源管理器和设备对象聚合
        device = PDFPageAggregator(rsrcmagr, laparams=laparams)
        #创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmagr, device)
        last_para = '' # 记录上一段文本
        count = 0 # 对文本块进行计数，方便后续查找标题和作者
        author = '' # 记录作者
        ab_count = 0 # 记录已识别的摘要的数量，避免提取文中的abstract

        fanyi = YouDaoFanyi(appKey, appSecret)
        #循环遍历列表，每次处理一个page内容
        #doc.get_pages()获取page列表
        for page in doc.get_pages():
            interpreter.process_page(page)
            #接收该页面的LTPage对象
            layout = device.get_result()
            #这里的layout是一个LTPage对象 里面存放着page解析出来的各种对象
            #一般包括LTTextBox，LTFigure，LTImage，LTTextBoxHorizontal等等一些对像
            #想要获取文本就得获取对象的text属性
            for x in layout:
                try:
                    if(isinstance(x, LTTextBoxHorizontal)):
                        with open('%s' % (save_path), 'a', encoding='utf-8') as f:
                            result = x.get_text() # 每块的内容
                            # print(result)
                            # 提取标题
                            if count==0:
                                # 如果是researchgate的文章，直接翻页
                                if re.findall('^see discussions', result.lower())!=[]:
                                    break
                                # 如果第一行是各种页眉等干扰信息，直接略过
                                if re.findall('(^[0-9])|(^(research )?article)|(unclassified)|(www.)|(accepted (from|manuscript))|(proceedings of)|(vol.)|(volume \d)|(https?://)|(^ieee)|(sciencedirect)|(\d{4}\)$)|(\d{1,4} – \d{1,4}$)|(cid:)',re.split('\s+$',result.lower())[0])!=[] or '':
                                    count -= 1
                                else:
                                    # 将结果写入TXT
                                    f.write('\n'+result.replace('\n', '')+'\n')
                            # 提取作者
                            elif count==1:
                                # 只取第一作者
                                author = result.split('\n')[0].split(',')[0].split(' and ')[0]
                                author = generate_author(author)
                                print('author '+ author)
                            # 去掉pdf文件读取的各种换行符
                            result = result.replace('\n', '')
                            try:
                                # 转为小写，去掉空格，方便正则识别
                                last_para = last_para.lower().replace(' ', '')
                                # print(result)
                                # 匹配Abstract和摘要内容分开的情况
                                if re.findall('abstract$', last_para)!=[]:
                                    # 去掉关键词
                                    oringin_result = re.split('(K|k)(eyword|EYWORD)[sS]?',result)[0]
                                    # 翻译并转换人称
                                    trans_result = fanyi.translate(oringin_result).replace('我们', '他们')
                                    # print(result)
                                    # 组织语言写入TXT
                                    write_cont = author + '等人提出：' + trans_result + '\n'
                                    ab_count += 1
                                    f.write(write_cont)
                                # 匹配Abstract和摘要内容位于同一行的情况
                                elif re.findall('^abstract', result.lower().replace(' ', ''))!=[] and re.findall('abstract$', result.lower().replace(' ', ''))==[]:
                                    # 确保摘要只匹配一次，不匹配文中的Abstract字眼
                                    if ab_count==0:
                                        # 去掉Abstract字眼及其后续的符号
                                        oringin_result = re.sub('(a|A)(bstract|BSTRACT)[- —.]?','', result)
                                        # 去掉关键词
                                        oringin_result = re.split('(K|k)(eyword|EYWORD)[sS]?',oringin_result)[0]
                                        # 翻译并转换人称
                                        trans_result = fanyi.translate(oringin_result).replace('我们', '他们')
                                        # print(result)
                                        # 组织语言写入TXT
                                        write_cont = author + '等人提出：' + trans_result + '\n'
                                        ab_count += 1
                                        f.write(write_cont)
                                # 匹配结论
                                elif re.findall('(^(i|v|x|\d)*\.?conclusions?)|(conclusions?$)', last_para)!=[]:
                                        # 避免因图表在标题下方导致的识别错误
                                        if re.findall('^fig', result.lower()):
                                            continue
                                        # 翻译
                                        trans_result = fanyi.translate(result)
                                        # print(result)
                                        # 转换人称
                                        write_cont = trans_result.replace('我们', '他们') + '\n'
                                        # 写入TXT
                                        f.write(write_cont)
                            except Exception as e:
                                print(e)
                            last_para = result
                            count += 1
                except Exception as e:
                    print('out'+str(e))
            else:
                continue
        with open('%s' % (save_path), 'a', encoding='utf-8') as f:
            f.write('\n')
```
### 按照引用的格式生成作者信息
```python
def generate_author(author):
    # 过滤掉作者名后面的各种符号，并生成引用的格式
    # print(author)
    author = re.sub('by |[\s\d\*∗\/@†\(\&\)]+$', '', author)
    author_list = re.split('\s+',author)
    author_str = author_list[len(author_list)-1]
    for i in range(0,len(author_list)-1):
        author_str = author_str + ' ' + author_list[i][0]
    return author_str
```
### 翻译接口
其实直接抄有道官网文档就可以了，这里在其基础上做了更改：
```python
class YouDaoFanyi:
    def __init__(self, appKey, appSecret):
        self.YOUDAO_URL = 'https://openapi.youdao.com/api/'
        self.APP_KEY = appKey  # 应用id
        self.APP_SECRET = appSecret  # 应用密钥
        self.langFrom = 'en'   # 翻译前文字语言,auto为自动检查
        self.langTo = 'zh-CHS'     # 翻译后文字语言,auto为自动检查
        self.vocabId = "您的用户词表ID"

    def encrypt(self,signStr):
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(signStr.encode('utf-8'))
        return hash_algorithm.hexdigest()


    def truncate(self,q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

    def do_request(self,data):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return requests.post(self.YOUDAO_URL, data=data, headers=headers)


    def translate(self,q):
        data = {}
        data['from'] = self.langFrom
        data['to'] = self.langTo
        data['signType'] = 'v3'
        curtime = str(int(time.time()))
        data['curtime'] = curtime
        salt = str(uuid.uuid1())
        signStr = self.APP_KEY + self.truncate(q) + salt + curtime + self.APP_SECRET
        sign = self.encrypt(signStr)
        data['appKey'] = self.APP_KEY
        data['q'] = q
        data['salt'] = salt
        data['sign'] = sign
        data['vocabId'] = self.vocabId

        response = self.do_request(data)
        contentType = response.headers['Content-Type']
        result = json.loads(response.content.decode('utf-8'))['translation'][0]
        print(result)
        return result
```
最后，书写主函数进行调用：
```python
if __name__ == '__main__':
    #解析本地PDF文本，保存到本地TXT
    folder = '文件夹路径' # 需要读取pdf的文件夹的路径，注意为绝对路径，如：E:/论文/
    write_txt_file = 'result.txt' # 保存结果的文件
    appKey = '应用ID'  # 应用id
    appSecret = '应用秘钥'  # 应用密钥
    success_count = 0 # 统计成功的次数
    fail_count = 0 #统计失败的次数

    # 单次调用，供开发测试
    # pdf_filename = folder+'文件名'
    # with open(pdf_filename,'rb') as pdf_html:
    #     try:
    #         parse(pdf_html, folder + write_txt_file, appKey, appSecret)
    #         success_count+=1
    #     except Exception as e:
    #         print(pdf_filename)
    #         fail_count+=1

    pdf_list = getFileName(folder)
    # 依次读取元祖，获取pdf文件位置
    for file_item in pdf_list:
        with open(file_item,'rb') as pdf_html:
            try:
                print(file_item)
                parse(pdf_html, folder + write_txt_file, appKey, appSecret)
                success_count+=1
            except Exception as e:
                # 文件读取或翻译失败则将错误信息写入TXT
                print('文档读取失败：' + str(e) +'，路径为：' + file_item)
                with open('%s' % (folder + write_txt_file), 'a', encoding='utf-8') as f:
                    f.write('\n'+'文档读取失败：' + str(e) +'，路径为：' + file_item + '\n')
                fail_count+=1

    print('共读取pdf文件' + str(success_count+fail_count) + '个，其中成功读取并翻译' + str(success_count) + '个，失败' + str(fail_count) + '个')
```
至此，代码编写完毕
## 使用
代码可在[Github](https://github.com/you8023/Auto-Review-Generator)上下载
### 配置代码
更改代码主函数的配置变量（其中的应用ID和应用秘钥需要事先申请，见上文事前准备一节）：
```python
if __name__ == '__main__':
    #解析本地PDF文本，保存到本地TXT
    folder = '文件夹路径' # 需要读取pdf的文件夹的路径，注意为绝对路径，如：E:/论文/
    write_txt_file = 'result.txt' # 保存结果的文件
    appKey = '应用ID'  # 应用id
    appSecret = '应用秘钥'  # 应用密钥
```
### 运行代码
在代码所在的根目录下的命令行中输入以下命令即可：
```
python pdfprocessor.py
```
## 运行结果
仅花了38秒的时间，就提取并翻译完成了14个pdf文件，翻译生成的字数合计6812个字：

![运行结果](https://upload-images.jianshu.io/upload_images/5714082-6ebae187fdf9ac04.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

试了一下45个文件，花了大概两分钟，生成了一万多字

最后看一下翻译结果对比：

![翻译结果中英对比](https://upload-images.jianshu.io/upload_images/5714082-308ebb2f869973a9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

