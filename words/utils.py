import chardet
from urllib.parse import urlparse, urljoin
from words.models.article import Article



def to_abs_url(base, url):
    if base is None or url is None:
        return url
    elif 'url'.startswith('http:') or 'url'.startswith('https:'):
        return url
    elif 'url'.startswith('/'):
        s = urlparse(base)
        return s.schema + s.netloc + url
    else:
        return urljoin(base, url)


def extract_articles(response, parent_css, exclude=None):
    base_url = response.url
    for block in response.css(parent_css):
        for link in block.css('a'):
            titles = map(str.strip, link.css('::text').extract())
            title = "".join(titles)
            url = link.css('::attr("href")').extract_first()
            if title is not None and url is not None:
                title = title.strip()
                url = to_abs_url(base_url, url.strip())
                if exclude is not None:
                    if not exclude(title):
                        yield title, url
                else:
                    yield title, url

def get_article(response, parent_css):
    content = str()
    article_id = response.meta['id']
    article = Article.find(id=article_id)
    for block in response.css(parent_css):
        for paragraph in block.css('p'):
            texts = map(str.strip, paragraph.css('::text').extract())
            text = "".join(texts)
            content += text
    # print(text)
    print(article.title)
    article.update({'content': content})
    # c_art.update({'content': text})

def persist_article_abstract(source, title, url, city):
    article = Article.first_or_new_by_url(url)
    article.source = source
    article.title = title
    article.url = url
    article.tags = city
    article.save()
