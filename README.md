# file_download
下载matplotlib网站的样例源代码
## 前言
&ensp;&ensp;&ensp;&ensp;本文中如有错误，请指正。
## 背景
&ensp;&ensp;&ensp;&ensp;在上一篇文章中，给大家介绍了Scrapy下载文件和图片的理论内容（https://blog.csdn.net/xue605826153/article/details/85252026）， 本篇以matplotlib网站为例具体介绍下载文件的方法。
如图，下载每一个例子的源代码。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20181226140332854.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3h1ZTYwNTgyNjE1Mw==,size_16,color_FFFFFF,t_70)
## 码上行动
&ensp;&ensp;&ensp;&ensp;首先进行页面 https://matplotlib.org/examples/index.html, 可以看到些页面中列出了26个大类，每个大类下面都有样例，我们要做的就是下载这些样例的源代码。
&ensp;&ensp;&ensp;&ensp;通过xpath helper可以筛选出所有的样例，因此也能获得每个样例的链接。程序中通过链接提取器提取全部样例的链接，并循环访问每个链接以便提取每个样例的下载链接。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20181226140937751.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3h1ZTYwNTgyNjE1Mw==,size_16,color_FFFFFF,t_70)
&ensp;&ensp;&ensp;&ensp;随意点开一个样例，可以看到网页中的下载源代码的按键。我们只需要把对应的链接放入item['file_urls']，并进行相应配置即可下载对应的文件。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20181226141201326.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3h1ZTYwNTgyNjE1Mw==,size_16,color_FFFFFF,t_70)

 1. 提取所有样例的链接,并访问
 ```
     def parse(self, response):
        #le = LinkExtractor(restrict_css='div.toctree-wrapper.compound',deny='/index.html$')
        le = LinkExtractor(restrict_xpaths='//li[@class="toctree-l2"]/a')
        links = le.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url,callback=self.parse_down)
 ```
 2. 提取每一个样例的下载链接，并赋值给```item['file_urls']```(ps:```item['file_urls']```为一个列表)
 ```
    def parse_down(self,response):
        item = DownloadItem()
        href = response.xpath('//a[@class="reference external"]/@href').extract_first()
        item['file_urls'] = [response.urljoin(href)]

        yield item
```
&ensp;&ensp;&ensp;&ensp;按理论部分所讲，如果直接配置item和settings.py进行下载，下载文件的名字将是一串长度相等的奇怪数字，这些数字是下载文件url的sha1散列值，并且所有文件都是在一个文件夹中，我们不能直观的快捷的找出自己想要的那一个文件。因此需要为每个文件改一个直观的名字，并按网页上的大类，进行下载，每一类在一个文件夹中。
&ensp;&ensp;&ensp;&ensp;查看资料可知，file_path方法决定了文件的命名。因些实现一个FilesPipeline的子类，覆写file_path方法来实现所期望的文件命名规则。观察每一个下载链接可以发现是有规律的。以 https://matplotlib.org/examples/animation/animate_decay.py 为例 ，该链接最后为文件名，倒数第二个为分类。因此我们可以利用此规律进行重命名。
```
# pipeline部分
from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse
from os.path import basename,dirname,join

class DownloadPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        path = urlparse(request.url).path
        return join(basename(dirname(path)),basename(path))
```
&ensp;&ensp;&ensp;&ensp;settings部分为：
```
ITEM_PIPELINES = {
   'download.pipelines.DownloadPipeline': 1,
}
FILES_STORE = 'download/files'
```
## 后语
1. 下载结果信息为：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20181226144004553.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3h1ZTYwNTgyNjE1Mw==,size_16,color_FFFFFF,t_70)
2. 下载结果如图所示（部分）：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20181226145429646.png)
3. 仔细对比可以发现，本篇第一图中拿到的链接对应每个样例的详情页，而将链接最后的 html 改为 py 即为该样例的下载链接。仔细对比可以发现，本篇第一图中拿到的链接对应每个样例的详情页，而将链接最后的 html 改为 py 即为该样例的下载链接。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20181226143612790.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3h1ZTYwNTgyNjE1Mw==,size_16,color_FFFFFF,t_70)
