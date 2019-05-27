from orator import Model


class Article(Model):
    __guarded__ = ['id']

    @staticmethod
    def first_or_new_by_url(url):
        article = Article.where('url', '=', url).first()
        if article is None:
            article = Article()
            article.url = url
        return article

    @staticmethod
    def get_null_content(source):
        article = Article.where('source', '=', source).where_null('url')
        if article is None:
            article = Article()
        return article
