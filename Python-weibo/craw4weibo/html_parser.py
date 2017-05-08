import sys
import os
import requests
import time
from lxml import etree


class HtmlParser(object):

    def _save_user_data(self, url):
        res_url = url.split("/")
        num = len(res_url)
        user_id = res_url[num - 1]
        url = "%s?filter=1" % url
        print url

        cookie = {}
        #headers = ""
        #get web page using request
        response = requests.get(url, cookies=cookie)
        print "code:", response.status_code
        html_cont = response.content
        # get current user_id
        res_url = url.split("/")
        num = len(res_url)
        user_id = res_url[num - 1]
        #print user_id
        selector = etree.HTML(html_cont)
        #print selector.xpath('//input[@name="mp"]')
        #get page of the weibo
        pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
        print "page",pageNum
        result = ""
        word_count = 1
        times = 5
        one_step = pageNum / times
        for step in range(times):
            if step < times - 1:
                i = step * one_step + 1
                j = (step + 1) * one_step + 1
            else:
                i = step * one_step + 1
                j = pageNum + 1
            for page in range(i, j):
                try:
                    #download weibo of certain page
                    url = 'https://weibo.cn/%s?filter=1&page=%d' % (user_id, page)
                    #print url
                    lxml = requests.get(url, cookies=cookie).content
                    selector = etree.HTML(lxml)
                    content = selector.xpath('//span[@class="ctt"]')
                    for each in content:
                        text = each.xpath('string(.)')
                        #print text
                        if word_count >= 3:
                            text = "%d: " % (word_count - 2) + text + "\n"
                        else:
                            text = text + "\n\n"
                        print text
                        result = result + text
                        word_count += 1
                    print 'getting',page, ' page word ok!'
                    sys.stdout.flush()

                except:
                    print page, 'error'
                print page, 'sleep'
                sys.stdout.flush()
                time.sleep(3)
            print 'continuing', step + 1, 'stopping'
            time.sleep(10)

        try:
            #print "1"
            file_name = "%s.txt" % user_id
            fo = open(file_name, "wb")
            #print "2"
            fo.write(result.encode('utf-8'))
            #print "3"
            fo.close()
            print 'finishing word spiderring'
        except:
            print 'cannot find adress'
        sys.stdout.flush()

    def _get_new_urls(self, url):
        new_urls = set()
        res_url = url.split("/")
        num = len(res_url)
        user_id = res_url[num - 1]
        cookie = {}
        headers = "#Your header"
        url = 'https://weibo.cn/%s/follow' % user_id
        response = requests.get(url, cookies=cookie).content
        selector = etree.HTML(response)
        pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])

        times = 5
        one_step = pageNum / times
        for step in range(times):
            if step < times - 1:
                i = step * one_step + 1
                j = (step + 1) * one_step + 1
            else:
                i = step * one_step + 1
                j = pageNum + 1
            for page in range(i, j):
                try:
                    url = 'https://weibo.cn/%s/follow?page=%d' % (user_id, page)
                    lxml = requests.get(url, cookies=cookie).content
                    selector = etree.HTML(lxml)
                    content = selector.xpath('/html/body/table/tr/td[2]/a[1]')
                    for c in content:
                        temp_url = c.attrib['href']
                        if temp_url is not None:
                            new_urls.add(temp_url)
                    print 'geint follow',page, 'page word ok!'
                    sys.stdout.flush()

                except:
                    print page, 'error'
                print page, 'sleep'
                sys.stdout.flush()
                time.sleep(3)
            print 'continuing', step + 1, 'stopping'
            time.sleep(10)

        return new_urls

    def parse(self, url):

        if url is None:
            return
        print "saving"
        try:
            self._save_user_data(url)
        except:
            print "error in saving %s" % url
        print "getting"
        try:
            new_urls = self._get_new_urls(url)
        except:
            print "error in getting %s" % url
        print "finishing"
        return new_urls

