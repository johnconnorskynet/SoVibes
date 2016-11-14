from parser import parser
url = 'http://mashable.com'

site_parser = parser.get_parser(url)
site_parser.parse(url)