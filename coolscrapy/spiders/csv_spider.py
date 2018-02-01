from scrapy.spiders import CSVFeedSpider

from coolscrapy.items import CSVItem


class CSVSpider(CSVFeedSpider):
    name = 'csv'
    allowed_domains = ['127.0.0.1']
    start_urls = ['http://127.0.0.1/fbaccount3.csv']
    delimiter = ','#每行的分隔符
    quotechar = "'"
    headers = ['id','username','password','birth','userid','status','ip','fname',
               'lname','sex','city','friendnum','requestnum','lastlogintime','lastrequesttime',
               'lasttagtime','advproduct','occupied','cookie'] #为csv的表头信息

    def parse_row(self, response, row):
        self.logger.info('Hi,this is a row!:%r',row)
        item = CSVItem()
        item['id'] = row['id']
        item['username'] = row['username']
        item['password'] = row['password']
        item['birth'] = row['birth']
        item['userid'] = row['userid']
        item['status'] = row['status']
        item['ip'] = row['ip']
        item['fname'] = row['fname']
        item['lname'] = row['lname']
        item['sex'] = row['sex']
        item['city'] = row['city']
        item['friendnum'] = row['friendnum']
        item['requestnum'] = row['requestnum']
        item['lastlogintime'] = row['lastlogintime']
        item['lastrequesttime'] = row['lastrequesttime']
        item['lasttagtime'] = row['lasttagtime']
        item['advproduct'] = row['advproduct']
        item['occupied'] = row['occupied']
        item['cookie'] = row['cookie']
        yield item

