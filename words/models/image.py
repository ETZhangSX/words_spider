from orator import Model


class Image(Model):
    __guarded__ = ['id']

    @staticmethod
    def find_or_create_by_artile_id_and_url(article_id, url):
        image = Image.where('article_id', '=', article_id).where('original_url', '=', url).first()
        if image is None:
            image = Image()
            image.article_id = article_id
            image.original_url = url
        return image
