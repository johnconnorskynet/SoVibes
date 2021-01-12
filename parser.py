

class parser(object):

    @staticmethod
    def get_parser(url):
        if 'mashable' in url:
            return mashable_parser()
        elif 'theverge' in url:
            pass
