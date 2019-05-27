# words_spider
软件工程课设爬虫部分

## 选题
**课题方向:**
海量词库构建

**课题背景:**
目前随着互联网及通信技术的发展，各类数据极具膨胀，为了有效对文本信息进行分析，需要构建海量中文词库，目前互联网上公开的词库量太少，需要构建千万级海量词库，从一些公开的网站以及算法中迭代构建，从而有效支持中文分词，更好把握文本中的关键信息，以及后续的语义分析。

## 安装部署

安装爬虫项目需要的库，本项目使用的是scrapy框架
```shell
pip install -r requirements.txt
```
`config`中为数据库配置文件，通过修改`DATABASE`为本地数据库配置连接使用

`words_spider.sql`为本项目MySQL数据库结构迁移文件，生成本爬虫项目所需数据库结构，终端执行：
```shell
mysql -uroot -p < words_spider.sql
```
其中`root`为用户名，输入密码后即可导入

### 运行项目(本地运行)

`scrapy.cfg`为scrapy部署配置文件，如需部署到服务器，修改配置文件即可

进入项目路径，启动scrapyd服务，挂起
```shell
cd project_path
scrapyd
```
新建终端窗口，进入项目目录
```shell
cd project_path
python setup.py install
scrapyd-deploy server -p words
```
即上传项目，完成部署

### API
命令行通过curl命令请求相应API接口

**启动爬虫**
```shell
curl http://localhost:6800/schedule.json -d project=words -d spider=sina
curl http://localhost:6800/schedule.json -d project=words -d spider=sina_article
```
项目包含两个爬虫

    -sina爬取新浪网页面的文章链接并存储到数据库
    -sina_article访问数据库获取sina爬取的链接并爬取页面文章存储到数据库中

**取消运行**
关闭与jobnumber对应的任务
```shell
curl http://localhost:6800/cancel.json -d project=words_spider -d job=jobnumber
```