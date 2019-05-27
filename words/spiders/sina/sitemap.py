import yaml
from pkg_resources import resource_string

sitemap = None
# with open(os.path.dirname(os.path.realpath(__file__)) + '/sitemap.yaml', 'r') as f:
#     sitemap = yaml.load(f)
sitemap = yaml.load(resource_string(__name__, 'sitemap.yaml'), Loader=yaml.FullLoader)
# sitemap = yaml.load('words/spiders/sina/sitemap.yaml')