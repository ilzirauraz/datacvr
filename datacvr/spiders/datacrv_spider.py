import scrapy
import datacvr.helpers.formating_data as fd
import datacvr.mongo.conn as mongo


class QuotesSpider(scrapy.Spider):
    name = "datacvr"
    success_cookies = {}
    meta = {'dont_redirect': True, 'handle_httpstatus_list': [302]}

    def start_requests(self):
        urls = [
            f'https://datacvr.virk.dk/data/visninger?page={number}' \
            f'&branche=&language=en-gb&ophoert=null&oprettet=null&soeg=&type=undefined'
            for number in range(0, 100)
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, method='GET',
                                 meta=self.meta, dont_filter=True, cookies=self.success_cookies)

    def parse(self, response):
        cvrs = []
        headers_dict = dict(
            (k.decode('utf-8'), v[0].decode('utf-8')) for k, v in list(response.headers.items()))

        if response.status == 302:
            location = headers_dict['Location']
            cookies = self._parse_cookie(headers_dict)

            yield scrapy.Request(url=location, callback=self.parse, method='GET', meta=self.meta,
                                      dont_filter=True, cookies=cookies)

        if response.status == 200:
            if self.success_cookies == {}:
                self.success_cookies.update(self._parse_cookie(headers_dict))
            cvrs += response.xpath('//*[@class="cvr"]/p/text()').getall()
            cvr_urls = [
                f'https://datacvr.virk.dk/data/index.php?enhedstype=virksomhed&id={cvr}' \
                f'&language=en-gb&type=undefined&q=visenhed' for cvr in cvrs]
            for cvr_url in cvr_urls:
                yield scrapy.Request(url=cvr_url, callback=self.get_company_info, method='GET', meta=self.meta,
                                     dont_filter=True, cookies=self.success_cookies)

    def get_company_info(self, response):
        company = fd.parse_tables(response)
        mongo_client = mongo.open_connection()
        mongo_client.datacvr.items.insert(company)

    def _parse_cookie(self, headers):
        elements = headers['Set-Cookie'].split(';')
        cookies = {}
        for element in elements:
            if len(element.split('='))>2:
                cookies.update({element.split('=')[0]: element.split('=')[1]})

        return cookies


