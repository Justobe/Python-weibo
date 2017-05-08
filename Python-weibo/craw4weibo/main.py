from craw4weibo import html_parser,url_manager

class SpiderMain(object):

    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.parser = html_parser.HtmlParser()

    def craw(self, uid):
        count = 1
        root_url = 'https://weibo.cn/%s' % uid
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print 'craw %d : %s' % (count, new_url)
                new_urls = self.parser.parse(new_url)
                self.urls.add_new_urls(new_urls)

                if count == 1:
                    break
                count = count + 1
            except:
                print "craw failed"


if __name__ == "__main__":

    root_uid = "Your root id"
    spider = SpiderMain()
    spider.craw(root_uid)


